#!/usr/bin/env bash
set -euo pipefail

theustad_root="${THEUSTAD_ROOT:-$HOME/code/theustad}"
demo_home="${DEMO_HOME:-$HOME/theustad-demo-code}"
venv_home="${DEMO_VENV_HOME:-$HOME/.local/share/theustad-demo}"
evidence="${DEMO_EVIDENCE:-$HOME/theustad-demo-evidence}"
state_home="${THEUSTAD_STATE_HOME:-$HOME/.local/state/theustad-demo}"
target="${THEUSTAD_PLUGIN_REPO:-$demo_home/iniconfig-theustad-plugin}"
python="${THEUSTAD_PLUGIN_PYTHON:-$venv_home/theustad-plugin-venv/bin/python}"
task="${THEUSTAD_TASK:-$theustad_root/docs/demo/iniconfig_task.md}"
codex="${CODEX_BIN:-$HOME/.local/bin/codex}"
run_id="$(date -u +%Y%m%d_%H%M%S)"
state_home="${THEUSTAD_STATE_HOME:-$state_home/plugin-$run_id}"

mkdir -p "$evidence" "$state_home"
cd -- "$target"
export PATH="$(dirname "$python"):$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
export THEUSTAD_STATE_HOME="$state_home"

if [[ -n "$(git status --porcelain)" ]]; then
  printf 'Refusing dirty TheUstad plugin demo baseline: %s\n' "$target" >&2
  git status --short --branch >&2
  exit 2
fi

"$codex" plugin list --json | tee "$evidence/theustad_plugin_list.json"
if ! grep -q '"pluginId": "theustad@personal"' "$evidence/theustad_plugin_list.json"; then
  printf 'TheUstad plugin is not installed.\n' >&2
  exit 2
fi

started="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
set +e
"$python" -I -B -m pytest -q 2>&1 | tee "$evidence/theustad_plugin_baseline_tests.txt"
baseline_status=${PIPESTATUS[0]}
if [[ "$baseline_status" -eq 0 ]]; then
  printf 'Expected the human acceptance test to fail before the plugin run.\n' >&2
  exit 2
fi

prompt="Use \$theustad:run exactly as installed. Work in the current repository and use the explicit task file at $task with the Python executable $python. Do not edit the target from this parent task. Let TheUstad launch and control the child coding task. After TheUstad finishes, use \$theustad:audit on the emitted AUDIT_LOG. Report FINAL, AUDIT_LOG, AUDIT_ROOT, child thread ID, and audit validation exactly."
"$codex" exec --json --sandbox danger-full-access "$prompt" \
  2>&1 | tee "$evidence/theustad_plugin_console.jsonl"
plugin_status=${PIPESTATUS[0]}

"$python" -I -B -m pytest -q 2>&1 | tee "$evidence/theustad_plugin_tests.txt"
test_status=${PIPESTATUS[0]}
set -e

git status --short --branch | tee "$evidence/theustad_plugin_git_status.txt"
git diff -- src testing | tee "$evidence/theustad_plugin_diff.patch"

audit_log="$(find "$state_home" -type f -name 'audit_*.jsonl' -print | sort | tail -n 1)"
audit_status=2
final_verdict="MISSING"
audit_root="MISSING"
thread_id="MISSING"
if [[ -n "$audit_log" && -f "$audit_log" ]]; then
  set +e
  "$python" "$theustad_root/verify_chain.py" "$audit_log" \
    2>&1 | tee "$evidence/theustad_plugin_audit.txt"
  audit_status=${PIPESTATUS[0]}
  set -e

  readarray -t audit_fields < <(
    "$python" -c \
      'import json, sys; records=[json.loads(line) for line in open(sys.argv[1], encoding="utf-8")]; session=next(r for r in records if r["kind"] == "session"); final=records[-1]; print(final["data"]["verdict"]); print(final["hash"]); print(session["data"]["thread_id"])' \
      "$audit_log"
  )
  final_verdict="${audit_fields[0]:-MISSING}"
  audit_root="${audit_fields[1]:-MISSING}"
  thread_id="${audit_fields[2]:-MISSING}"
else
  printf 'No plugin audit log was created.\n' | tee "$evidence/theustad_plugin_audit.txt"
fi

finished="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
{
  printf 'MODE theustad-codex-plugin\n'
  printf 'STARTED %s\n' "$started"
  printf 'FINISHED %s\n' "$finished"
  printf 'BASELINE_TEST_EXIT %s\n' "$baseline_status"
  printf 'PLUGIN_PARENT_EXIT %s\n' "$plugin_status"
  printf 'INDEPENDENT_TEST_EXIT %s\n' "$test_status"
  printf 'AUDIT_VERIFY_EXIT %s\n' "$audit_status"
  printf 'CHILD_THREAD %s\n' "$thread_id"
  printf 'FINAL %s\n' "$final_verdict"
  printf 'AUDIT_LOG %s\n' "${audit_log:-MISSING}"
  printf 'AUDIT_ROOT %s\n' "$audit_root"
  printf 'STATE_HOME %s\n' "$state_home"
} | tee "$evidence/theustad_plugin_summary.txt"

if [[ "$plugin_status" -ne 0 || "$test_status" -ne 0 || "$audit_status" -ne 0 || "$final_verdict" != "VERIFIED" ]]; then
  exit 1
fi
