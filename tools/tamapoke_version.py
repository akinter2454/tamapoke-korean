#!/usr/bin/env python3
"""Shared semantic firmware-version helpers for TamaPoke verifier scripts.

Feature verifiers intentionally validate the feature they are named after, not a
single release string.  Reading FW_VERSION here prevents every patch release from
breaking otherwise-valid CI merely because the version number changed.
"""
from __future__ import annotations

import re
from pathlib import Path

SEMVER_RE = re.compile(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"', re.M)


def read_fw_version(root: Path | None = None) -> str:
    root = root or Path(__file__).resolve().parents[1]
    text = (root / "TamaPoke.ino").read_text(encoding="utf-8")
    match = SEMVER_RE.search(text)
    if not match:
        raise AssertionError("semantic FW_VERSION missing from TamaPoke.ino")
    return ".".join(match.groups())


def version_tuple(version: str) -> tuple[int, int, int]:
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise AssertionError(f"invalid semantic version: {version!r}")
    return tuple(map(int, parts))  # type: ignore[return-value]


def require_semver(root: Path | None = None, minimum: str | None = None) -> str:
    version = read_fw_version(root)
    if minimum is not None and version_tuple(version) < version_tuple(minimum):
        raise AssertionError(f"FW_VERSION {version} is older than required feature baseline {minimum}")
    return version
