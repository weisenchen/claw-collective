"""Secret scanner — heuristic detection of API keys, tokens, and passwords.

Exit codes:
  0 = clean
  3 = secrets found (blocks commit/push)
"""

from __future__ import annotations

import os
import re
from pathlib import Path

# High-signal regex patterns
PATTERNS: list[tuple[str, re.Pattern]] = [
    ("private_key_block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z\-_]{30,}\b")),
    ("generic_secret", re.compile(
        r"(?i)\b(pass(word)?|pwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"]?[^\s'\"]{6,}"
    )),
]

SCAN_EXTS = {".md", ".txt", ".json", ".yml", ".yaml", ".js", ".ts", ".sh", ".py", ".env", ".toml", ""}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "_reference"}
SKIP_FILES = {"hosts.yml", "known_hosts"}

Finding = tuple[str, str, int, str]  # (label, relative_path, line_no, snippet)


def scan_directory(root: Path) -> list[Finding]:
    """Scan a directory tree for potential secrets. Returns list of findings."""
    findings: list[Finding] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.name in SKIP_FILES:
                continue
            try:
                if p.stat().st_size > 2_000_000:
                    continue
            except FileNotFoundError:
                continue
            if p.suffix.lower() not in SCAN_EXTS:
                continue
            # Skip binary files
            try:
                data = p.read_bytes()[:2048]
                if b"\x00" in data:
                    continue
            except Exception:
                continue

            try:
                text = p.read_text("utf-8", errors="replace")
            except Exception:
                continue

            rel = str(p.relative_to(root))
            for label, rx in PATTERNS:
                for m in rx.finditer(text):
                    line_no = text[: m.start()].count("\n") + 1
                    snippet = m.group(0)[:120]
                    findings.append((label, rel, line_no, snippet))

    return findings


def scan_and_report(root: Path) -> int:
    """Scan and print report. Returns 0 if clean, 3 if secrets found."""
    findings = scan_directory(root)
    if not findings:
        print("✅ No secrets detected")
        return 0

    print("🚫 POTENTIAL SECRETS DETECTED — blocking commit/push")
    print("Review and remove/redact these:")
    for label, rel, line_no, snippet in findings[:200]:
        print(f"  - {label}: {rel}:{line_no}: {snippet}")
    if len(findings) > 200:
        print(f"  … plus {len(findings) - 200} more")
    return 3
