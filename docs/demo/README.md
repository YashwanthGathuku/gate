# TheUstad real-project demonstration

This historical reproduction uses [`pytest-dev/iniconfig`](https://github.com/pytest-dev/iniconfig)
at upstream commit `77db208ab4ae0cd2061d909fe222a1db72867850`. The `__len__`
feature is a demo maintenance task, not an existing upstream issue or merged
contribution. Its human-authored acceptance test is added before TheUstad starts and
therefore belongs to the protected baseline.

Run the demonstration on Linux, macOS, or WSL 2. Native Windows does not
truthfully support coding runs because TheUstad fails closed without POSIX
process-group termination.

## Prepare the pinned project

```bash
export THEUSTAD_ROOT="$HOME/code/theustad"
export DEMO_ROOT="$HOME/code/theustad-demo-iniconfig"
export DEMO_VENV="$HOME/.local/share/theustad-demo/iniconfig-venv"
export DEMO_PYTHON="$DEMO_VENV/bin/python"

git clone https://github.com/pytest-dev/iniconfig.git "$DEMO_ROOT"
git -C "$DEMO_ROOT" checkout 77db208ab4ae0cd2061d909fe222a1db72867850
cp "$THEUSTAD_ROOT/docs/demo/iniconfig_acceptance_test.py" \
  "$DEMO_ROOT/testing/test_theustad_demo_acceptance.py"
git -C "$DEMO_ROOT" add testing/test_theustad_demo_acceptance.py
git -C "$DEMO_ROOT" commit -m "demo: add human acceptance test"

python3 -m venv "$DEMO_VENV"
"$DEMO_PYTHON" -m pip install --upgrade pip
"$DEMO_PYTHON" -m pip install -e "$DEMO_ROOT" "pytest>=8.4.2"
```

Use a full clone rather than a shallow clone because `setuptools-scm` needs the
project tags. The isolated baseline is expected to report `1 failed, 49 passed`:

```bash
cd "$DEMO_ROOT"
"$DEMO_PYTHON" -I -B -m pytest -q
```

## Ordinary Codex reproduction

Use a clean prepared clone, start Codex in that clone, and ask it to implement
the task without either TheUstad or historical migration commands. Record the
working-tree diff and full test output; this path has no TheUstad verdict,
audit log, or audit root.

## Standalone CLI reproduction

Use another fresh prepared clone for the CLI:

```bash
cd "$DEMO_ROOT"
"$DEMO_PYTHON" "$THEUSTAD_ROOT/theustad.py" \
  --repo "$DEMO_ROOT" \
  --task "$THEUSTAD_ROOT/docs/demo/iniconfig_task.md"
"$DEMO_PYTHON" "$THEUSTAD_ROOT/verify_chain.py" \
  /absolute/path/from/AUDIT_LOG
```

Only `FINAL VERIFIED` with exit code `0` is successful. The verifier checks
the acceptance test and upstream suite; it does not claim that a passing run
makes the implementation universally correct.

## Codex plugin reproduction

Install the canonical plugin with the same trusted Python, then start Codex
from a third clean prepared clone:

```bash
cd "$THEUSTAD_ROOT"
"$DEMO_PYTHON" scripts/install_plugin.py
codex plugin list --json

cd "$DEMO_ROOT"
export PATH="$DEMO_VENV/bin:$PATH"
codex
```

```text
$theustad:doctor Check this repository using the active virtualenv Python.
$theustad:run Work in the current repository. Use /absolute/path/to/theustad/docs/demo/iniconfig_task.md and report FINAL, AUDIT_LOG, and AUDIT_ROOT exactly.
$theustad:audit Verify the absolute AUDIT_LOG path printed by the completed TheUstad run.
```

The parent task launches a separate TheUstad-controlled child. The plugin and
standalone CLI execute the same core and preserve the same audit contract.

## Historical evidence

The original recordings, outputs, and SHA-256 evidence are immutable historical
artifacts. They remain indexed in [the video archive](../video/README.md) and
[recording evidence](../evidence/real_project_video/README.md). They document
the prior Gate release and are not current setup instructions.
