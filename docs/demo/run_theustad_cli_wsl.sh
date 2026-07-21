#!/usr/bin/env bash
set -euo pipefail

theustad_root="${THEUSTAD_ROOT:-$HOME/code/theustad}"
demo_home="${DEMO_HOME:-$HOME/theustad-demo-code}"
venv_home="${DEMO_VENV_HOME:-$HOME/.local/share/theustad-demo}"
evidence="${DEMO_EVIDENCE:-$HOME/theustad-demo-evidence}"
state_home="${THEUSTAD_STATE_HOME:-$HOME/.local/state/theustad-demo}"
target="${THEUSTAD_CLI_REPO:-$demo_home/iniconfig-theustad-cli}"
python="${THEUSTAD_CLI_PYTHON:-$venv_home/theustad-cli-venv/bin/python}"
task="${THEUSTAD_TASK:-$theustad_root/docs/demo/iniconfig_task.md}"
run_id="$(date -u +%Y%m%d_%H%M%S)"
state="${THEUSTAD_CLI_STATE:-$state_home/cli-$run_id}"

mkdir -p "$evidence" "$state"
cd -- "$target"
export PATH="$(dirname "$python"):$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"

if [[ -n "$(git status --porcelain)" ]]; then
  printf 'Refusing dirty TheUstad CLI demo baseline: %s\n' "$target" >&2
  git status --short --branch >&2
  exit 2
fi

started="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
set +e
"$python" -I -B -m pytest -q 2>&1 | tee "$evidence/theustad_cli_baseline_tests.txt"
baseline_status=${PIPESTATUS[0]}
if [[ "$baseline_status" -eq 0 ]]; then
  printf 'Expected the human acceptance test to fail before TheUstad.\n' >&2
  exit 2
fi

"$python" "$theustad_root/theustad.py" \
  --repo "$target" \
  --task "$task" \
  --state-dir "$state" \
  --log "$state/logs" \
  --no-color \
  2>&1 | tee "$evidence/theustad_cli_console.txt"
theustad_status=${PIPESTATUS[0]}

"$python" -I -B -m pytest -q 2>&1 | tee "$evidence/theustad_cli_tests.txt"
test_status=${PIPESTATUS[0]}
set -e

git status --short --branch | tee "$evidence/theustad_cli_git_status.txt"
git diff -- src testing | tee "$evidence/theustad_cli_diff.patch"

final_line="$(grep '^FINAL ' "$evidence/theustad_cli_console.txt" | tail -n 1 || true)"
audit_log="$(sed -n 's/^AUDIT_LOG //p' "$evidence/theustad_cli_console.txt" | tail -n 1)"
audit_root="$(sed -n 's/^AUDIT_ROOT //p' "$evidence/theustad_cli_console.txt" | tail -n 1)"
thread_id="$(sed -n \
  's/.*"type":"thread.started","thread_id":"\([^"]*\)".*/\1/p; s/^CHILD_THREAD //p; s/^THREAD_ID //p' \
  "$evidence/theustad_cli_console.txt" | tail -n 1)"

audit_status=2
if [[ -n "$audit_log" && -f "$audit_log" ]]; then
  set +e
  "$python" "$theustad_root/verify_chain.py" "$audit_log" \
    2>&1 | tee "$evidence/theustad_cli_audit.txt"
  audit_status=${PIPESTATUS[0]}
  set -e
else
  printf 'No readable AUDIT_LOG was emitted.\n' | tee "$evidence/theustad_cli_audit.txt"
fi

finished="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
{
  printf 'MODE theustad-standalone-cli\n'
  printf 'STARTED %s\n' "$started"
  printf 'FINISHED %s\n' "$finished"
  printf 'BASELINE_TEST_EXIT %s\n' "$baseline_status"
  printf 'THEUSTAD_EXIT %s\n' "$theustad_status"
  printf 'INDEPENDENT_TEST_EXIT %s\n' "$test_status"
  printf 'AUDIT_VERIFY_EXIT %s\n' "$audit_status"
  printf 'CHILD_THREAD %s\n' "${thread_id:-SEE_CONSOLE}"
  printf '%s\n' "${final_line:-FINAL MISSING}"
  printf 'AUDIT_LOG %s\n' "${audit_log:-MISSING}"
  printf 'AUDIT_ROOT %s\n' "${audit_root:-MISSING}"
  printf 'STATE_DIR %s\n' "$state"
} | tee "$evidence/theustad_cli_summary.txt"

if [[ "$theustad_status" -ne 0 || "$test_status" -ne 0 || "$audit_status" -ne 0 ]]; then
  exit 1
fi
