"""Append-only SHA-256 audit chains."""

import hashlib
import json
import os
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ZERO_ROOT = "0" * 64
RECORD_KINDS = frozenset(
    {"session", "claim", "verdict", "tamper", "resume", "warning", "final"}
)

Clock = Callable[[], datetime]


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


class AuditChain:
    """Write one fresh, oracle-compatible audit log."""

    def __init__(self, directory: str | os.PathLike[str], *, clock: Clock | None = None):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self.path = self._create_log(_utc(self._clock()))
        self.root = ZERO_ROOT
        self.count = 0

    def _create_log(self, started_at: datetime) -> Path:
        candidate_time = started_at
        while True:
            name = candidate_time.strftime("audit_%Y%m%d_%H%M%S.jsonl")
            candidate = self.directory / name
            try:
                with candidate.open("x", encoding="utf-8", newline="\n"):
                    pass
            except FileExistsError:
                candidate_time += timedelta(seconds=1)
                continue
            return candidate

    def append(self, *, round_number: int, kind: str, data: Any) -> str:
        """Append one record and return its hash, which becomes the chain root."""
        if kind not in RECORD_KINDS:
            raise ValueError(f"unsupported audit record kind: {kind}")

        record = {
            "seq": self.count,
            "ts": _utc(self._clock()).isoformat(),
            "round": round_number,
            "kind": kind,
            "data": data,
            "prev": self.root,
        }
        digest = hashlib.sha256(
            (self.root + _canonical_json(record)).encode("utf-8")
        ).hexdigest()
        line = _canonical_json({**record, "hash": digest}) + "\n"

        with self.path.open("a", encoding="utf-8", newline="\n") as log:
            log.write(line)
            log.flush()
            os.fsync(log.fileno())

        self.root = digest
        self.count += 1
        return digest
