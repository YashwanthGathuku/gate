import subprocess
import sys
from pathlib import Path

import gate
import theustad
from gatelib.chain import AuditChain as LegacyAuditChain
from theustadlib.chain import AuditChain


ROOT = Path(__file__).resolve().parents[1]


def test_legacy_imports_forward_to_canonical_objects():
    assert gate.GateRunner is theustad.GateRunner
    assert gate.Verdict is theustad.Verdict
    assert LegacyAuditChain is AuditChain


def test_legacy_cli_emits_deprecation_and_canonical_help():
    result = subprocess.run(
        [sys.executable, str(ROOT / "gate.py"), "--help"],
        capture_output=True,
        text=True,
        shell=False,
        check=False,
    )
    assert result.returncode == 0
    assert "GATE_DEPRECATED use theustad.py" in result.stderr
    assert "Verify coding-agent completion claims" in result.stdout
