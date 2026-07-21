from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "docs" / "demo"


def read_script(name):
    return (DEMO / name).read_text(encoding="utf-8")


def test_demo_scripts_use_canonical_names_and_mode_contracts():
    prepare_script = read_script("prepare_wsl_demo.sh")
    cli_script = read_script("run_theustad_cli_wsl.sh")
    plugin_script = read_script("run_theustad_plugin_wsl.sh")
    control_script = read_script("run_control_wsl.sh")

    assert "theustad.py" in cli_script
    assert "THEUSTAD_ROOT" in cli_script
    assert "THEUSTAD_STATE_HOME" in plugin_script
    assert "theustad@personal" in plugin_script
    assert "$theustad:run" in plugin_script
    assert "theustad.py" not in control_script
    assert "77db208ab4ae0cd2061d909fe222a1db72867850" in prepare_script


def test_subprocess_scripts_are_fail_closed_and_capture_execution_metadata():
    for name in (
        "prepare_wsl_demo.sh",
        "run_theustad_cli_wsl.sh",
        "run_theustad_plugin_wsl.sh",
        "run_control_wsl.sh",
    ):
        script = read_script(name)
        assert script.startswith("#!/usr/bin/env bash\nset -euo pipefail\n")
        assert "date -u" in script
        assert "_status=${PIPESTATUS[0]}" in script or "status=$?" in script
        assert "status --porcelain" in script


def test_preparation_records_identical_pinned_inputs_and_baseline_evidence():
    script = read_script("prepare_wsl_demo.sh")

    assert 'git -C "$target" switch --detach "$upstream_commit"' in script
    assert 'sha256sum "$acceptance_target"' in script
    assert 'git -C "$target" rev-parse HEAD' in script
    assert '1 failed, 49 passed' in script
    assert "BASELINE_TEST_EXIT" in script
    assert "BASELINE_COMMIT" in script
    assert "ACCEPTANCE_SHA256" in script


def test_ordinary_mode_explicitly_has_no_theustad_launcher():
    script = read_script("run_control_wsl.sh")

    assert "TheUstad" in script
    assert "THEUSTAD_VERDICT NONE" in script
    assert "AUDIT_LOG NONE" in script
    assert "AUDIT_ROOT NONE" in script
    assert "THEUSTAD_ROOT" in script
