import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RETIRED = "ga" + "te"
RETIRED_RE = re.compile(
    rf"(?i:\b{RETIRED}\b|{RETIRED}_|{RETIRED}lib\b)|{RETIRED.title()}(?=[A-Z])"
)


def tracked_files(*, root=ROOT):
    output = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        capture_output=True,
        check=True,
    ).stdout
    return [os.fsdecode(relative) for relative in output.split(b"\0") if relative]


def find_retired_names(files, *, root=ROOT):
    offenders = []
    for relative in files:
        if RETIRED in relative.lower():
            offenders.append(f"{relative}:path")
        path = root / relative
        if not path.is_file() or b"\0" in path.read_bytes()[:4096]:
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="surrogateescape").splitlines(),
            start=1,
        ):
            if RETIRED_RE.search(line):
                offenders.append(f"{relative}:{line_number}:{line.strip()}")
    return offenders


def test_repository_is_theustad_only():
    assert find_retired_names(tracked_files()) == []


def test_retired_name_in_path_is_reported(tmp_path):
    relative = f"{RETIRED}-dashboard.md"
    (tmp_path / relative).write_text("TheUstad\n", encoding="utf-8")
    assert find_retired_names([relative], root=tmp_path) == [f"{relative}:path"]


def test_retired_display_name_is_reported(tmp_path):
    relative = "README.md"
    line = f"Formerly {RETIRED.title()}"
    (tmp_path / relative).write_text(line + "\n", encoding="utf-8")
    assert find_retired_names([relative], root=tmp_path) == [
        f"{relative}:1:{line}"
    ]


def test_common_words_are_not_false_positives(tmp_path):
    relative = "LICENSE.txt"
    (tmp_path / relative).write_text(
        "Aggregate work may propagate changes.\n", encoding="utf-8"
    )
    assert find_retired_names([relative], root=tmp_path) == []
