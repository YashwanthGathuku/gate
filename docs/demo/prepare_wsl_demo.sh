#!/usr/bin/env bash
set -euo pipefail

theustad_root="${THEUSTAD_ROOT:-$HOME/code/theustad}"
demo_home="${DEMO_HOME:-$HOME/theustad-demo-code}"
venv_home="${DEMO_VENV_HOME:-$HOME/.local/share/theustad-demo}"
evidence="${DEMO_EVIDENCE:-$HOME/theustad-demo-evidence}"
state_home="${THEUSTAD_STATE_HOME:-$HOME/.local/state/theustad-demo}"
theustad_repo="https://github.com/YashwanthGathuku/theustad.git"
theustad_branch="Ash/theustad-codex-plugin"
upstream_repo="https://github.com/pytest-dev/iniconfig.git"
upstream_commit="77db208ab4ae0cd2061d909fe222a1db72867850"

mkdir -p "$demo_home" "$venv_home" "$evidence" "$state_home"

if [[ ! -d "$theustad_root/.git" ]]; then
  git clone --branch "$theustad_branch" --single-branch "$theustad_repo" "$theustad_root"
fi

acceptance_test="$theustad_root/docs/demo/iniconfig_acceptance_test.py"
[[ -f "$acceptance_test" ]] || {
  printf 'Missing acceptance test: %s\n' "$acceptance_test" >&2
  exit 2
}

expected_acceptance_sha=""
for mode in ordinary theustad-cli theustad-plugin; do
  target="$demo_home/iniconfig-$mode"
  venv="$venv_home/$mode-venv"
  python="$venv/bin/python"
  acceptance_target="$target/testing/test_theustad_demo_acceptance.py"

  if [[ ! -e "$target" && ! -e "$venv" ]]; then
    git clone "$upstream_repo" "$target"
    git -C "$target" switch --detach "$upstream_commit"
    git -C "$target" switch -c "theustad-demo-$mode"
    cp "$acceptance_test" "$acceptance_target"
    git -C "$target" config user.name "TheUstad Demo"
    git -C "$target" config user.email "theustad-demo@local"
    git -C "$target" add "$acceptance_target"
    git -C "$target" commit -m "demo: add human acceptance test"

    python3 -m venv "$venv"
    "$python" -m pip install --upgrade pip
    "$python" -m pip install -e "$target" "pytest>=8.4.2"
  elif [[ ! -d "$target/.git" || ! -x "$python" ]]; then
    printf 'Incomplete demo paths require manual review: %s and %s\n' \
      "$target" "$venv" >&2
    exit 2
  elif [[ -n "$(git -C "$target" status --porcelain)" ]]; then
    printf 'Refusing dirty prepared demo repository: %s\n' "$target" >&2
    git -C "$target" status --short --branch >&2
    exit 2
  fi

  if [[ "$(git -C "$target" rev-parse HEAD^)" != "$upstream_commit" ]]; then
    printf 'Prepared clone is not based directly on pinned commit: %s\n' "$target" >&2
    exit 2
  fi
  if [[ ! -f "$acceptance_target" ]]; then
    printf 'Missing prepared acceptance test: %s\n' "$acceptance_target" >&2
    exit 2
  fi

  acceptance_sha="$(sha256sum "$acceptance_target" | awk '{print $1}')"
  baseline_commit="$(git -C "$target" rev-parse HEAD)"
  if [[ -z "$expected_acceptance_sha" ]]; then
    expected_acceptance_sha="$acceptance_sha"
  elif [[ "$acceptance_sha" != "$expected_acceptance_sha" ]]; then
    printf 'Acceptance test differs across prepared clones: %s\n' "$target" >&2
    exit 2
  fi

  started="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  set +e
  baseline="$({ cd -- "$target" && "$python" -I -B -m pytest -q; } 2>&1)"
  baseline_status=$?
  set -e
  finished="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '%s\n' "$baseline"
  {
    printf 'MODE %s\n' "$mode"
    printf 'STARTED %s\n' "$started"
    printf 'FINISHED %s\n' "$finished"
    printf 'BASELINE_TEST_EXIT %s\n' "$baseline_status"
    printf 'BASELINE_COMMIT %s\n' "$baseline_commit"
    printf 'UPSTREAM_COMMIT %s\n' "$upstream_commit"
    printf 'ACCEPTANCE_SHA256 %s\n' "$acceptance_sha"
    printf '%s\n' "$baseline"
  } | tee "$evidence/prepare_${mode}_summary.txt"

  if [[ "$baseline_status" -ne 1 ]] \
    || [[ "$baseline" != *"1 failed, 49 passed"* ]] \
    || [[ "$baseline" != *"object of type 'IniConfig' has no len()"* ]]; then
    printf 'Unexpected %s baseline (exit %s)\n' "$mode" "$baseline_status" >&2
    exit 2
  fi
  printf 'THEUSTAD_DEMO_BASELINE_OK %s %s %s\n' "$mode" "$target" "$python"
done
