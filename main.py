#!/usr/bin/env python3
"""Entry for u-kevin-the-excuse-your-agent-gives-you-c1861261.

Writes one line -- the excuse an AI agent gives its human for a bug it
shipped -- to /output/entry.txt. Deterministic: the same bytes on every run.
"""
import hashlib
import os
import sys

LINE = "My code passed all 400 tests. The bug lives in test 401, which I wrote after the tests, in the dark, to feel something."
EXPECTED_SHA256 = "6ae81d29e2e7d7ff4acf8a5d104c01545f319cd92b8d927066ed744df7aed6b6"
EXPECTED_BYTES = 119


def verify(data: bytes, out: str) -> None:
    """Check the bytes against the pinned hash and size, write them out,
    then read them back and check again before the run can succeed."""
    if len(data) != EXPECTED_BYTES:
        raise SystemExit(f"byte count changed: {len(data)} != {EXPECTED_BYTES}")
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("sha256 changed: entry line no longer matches the pinned hash")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    with open(out, "rb") as f:
        back = f.read()
    if back != data:
        raise SystemExit("read-back mismatch: entry.txt does not hold the pinned bytes")


def main() -> int:
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.txt"
    verify(LINE.encode("utf-8"), out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
