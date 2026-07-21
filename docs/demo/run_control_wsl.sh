#!/usr/bin/env bash
set -euo pipefail

theustad_root="${THEUSTAD_ROOT:-$HOME/code/theustad}"
demo_home="${DEMO_HOME:-$HOME/theustad-demo-code}"
venv_home="${DEMO_VENV_HOME:-$HOME/.local/share/theustad-demo}"
evidence="${DEMO_EVIDENCE:-$HOME/theustad-demo-evidence}"
state_home="${THEUSTAD_STATE_HOME:-$HOME/.local/state/theustad-demo}"
target="${NO_THEUSTAD_REPO:-$demo_home/iniconfig-ordinary}"
python="${NO_THEUSTAD_PYTHON:-$venv_home/ordinary-venv/bin/python}"
task="${THEUSTAD_TASK:-$theustad_root/docs/demo/iniconfig_task.md}"
codex="${CODEX_BIN:-$HOME/.local/bin/codex}"

mkdir -p "$evidence"
cd -- "$target"
export PATH="$(dirname "$python"):$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"

if [[ -n "$(git status --porcelain)" ]]; then
  printf 'Refusing dirty ordinary demo baseline: %s\n' "$target" >&2
  git status --short --branch >&2
  exit 2
fi

started="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
set +e
"$codex" exec --json --sandbox workspace-write \
  "Work as ordinary Codex without TheUstad. Read and implement the task at $task in the current repository. Do not invoke any TheUstad skill or launcher. Do not create or report a TheUstad verdict, audit log, or audit root. Run the complete test suite and report what you changed and verified." \
  2>&1 | tee "$evidence/no_theustad_console.jsonl"
codex_status=${PIPESTATUS[0]}

"$python" -I -B -m pytest -q 2>&1 | tee "$evidence/no_theustad_tests.txt"
test_status=${PIPESTATUS[0]}
set -e

git status --short --branch | tee "$evidence/no_theustad_git_status.txt"
git diff -- src testing | tee "$evidence/no_theustad_diff.patch"
finished="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
  printf 'MODE ordinary-codex-without-theustad\n'
  printf 'STARTED %s\n' "$started"
  printf 'FINISHED %s\n' "$finished"
  printf 'CODEX_EXIT %s\n' "$codex_status"
  printf 'INDEPENDENT_TEST_EXIT %s\n' "$test_status"
  printf 'THEUSTAD_VERDICT NONE\n'
  printf 'AUDIT_LOG NONE\n'
  printf 'AUDIT_ROOT NONE\n'
} | tee "$evidence/no_theustad_summary.txt"

if [[ "$codex_status" -ne 0 || "$test_status" -ne 0 ]]; then
  exit 1
fi
