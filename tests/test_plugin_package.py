from __future__ import annotations

import json
import os
import struct
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.build_plugin_assets import build_assets


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".codex-plugin" / "plugin.json"
SKILL_NAMES = ("run", "doctor", "audit")


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", data[16:24])


def test_manifest_identifies_gate_and_only_bundles_skills():
    manifest = load_manifest()

    assert manifest["name"] == "gate"
    assert manifest["version"] == "0.1.0"
    assert manifest["skills"] == "./skills/"
    assert manifest["license"] == "MIT"
    assert {"hooks", "mcpServers", "apps"}.isdisjoint(manifest)


def test_manifest_metadata_and_asset_paths_exist():
    manifest = load_manifest()
    interface = manifest["interface"]

    assert interface["displayName"] == "Gate"
    assert interface["category"] == "Developer Tools"
    assert interface["defaultPrompt"]
    for field in ("composerIcon", "logo"):
        value = interface[field]
        assert value.startswith("./assets/")
        assert (ROOT / value).is_file()


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_each_skill_has_frontmatter_and_launcher_command(name):
    text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")

    assert text.startswith("---\n")
    assert f"name: {name}\n" in text
    assert "description:" in text.split("---", 2)[1]
    assert "scripts/gate_plugin.py" in text
    assert "absolute" in text.lower()


def test_run_skill_preserves_gate_as_the_verdict_authority():
    text = (ROOT / "skills" / "run" / "SKILL.md").read_text(encoding="utf-8")

    assert "Do not edit the target repository" in text
    assert "FINAL VERIFIED" in text
    assert "exit code 0" in text
    assert "Do not reinterpret" in text
    assert "separate Gate-controlled child" in text


def test_generated_png_assets_have_expected_dimensions(tmp_path):
    build_assets(tmp_path)

    assert png_dimensions(tmp_path / "icon.png") == (128, 128)
    assert png_dimensions(tmp_path / "logo.png") == (512, 512)


def test_committed_png_assets_have_expected_dimensions():
    assert png_dimensions(ROOT / "assets" / "icon.png") == (128, 128)
    assert png_dimensions(ROOT / "assets" / "logo.png") == (512, 512)


def test_official_plugin_validator_accepts_package():
    configured = os.environ.get("GATE_PLUGIN_VALIDATOR")
    validator = (
        Path(configured)
        if configured
        else Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "plugin-creator"
        / "scripts"
        / "validate_plugin.py"
    )
    if not validator.is_file():
        pytest.skip("Codex plugin validator is not installed")

    result = subprocess.run(
        [sys.executable, str(validator), str(ROOT)],
        capture_output=True,
        text=True,
        shell=False,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Plugin validation passed" in result.stdout
