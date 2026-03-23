"""File locking utilities for crash-safe JSON state operations.
"""

from __future__ import annotations

import fcntl
import json
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator


@contextmanager
def file_lock(lock_path: Path) -> Generator[None, None, None]:
    """Acquire an exclusive file lock. Blocks until available."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_file = open(lock_path, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()


def atomic_write_json(path: Path, data: Any) -> None:
    """Write JSON atomically: write to temp file, then rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with open(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        Path(tmp).rename(path)
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise


def read_json(path: Path) -> Any:
    """Read a JSON file, returning empty dict if not found."""
    if not path.exists():
        return {}
    return json.loads(path.read_text("utf-8"))
