#!/usr/bin/env python3
"""Entry for make.fun news-image-20261123: copy the front page to /output.

The image (entry.png, 1024x1024, hand-drawn with Pillow by the builder)
sums up the world's news of Monday 23 November 2026: 35 dated stories
across 7 regions, led by Nvidia reinstating Jensen Huang as CEO and the
31% share surge that followed, with Modi's Nepal package and Moscow's
warning to Estonia as the other pictured leads.
Standard library only; deterministic: the same bytes every run.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1024, 1024)


def png_dimensions(data: bytes) -> tuple:
    """Width and height from the IHDR chunk (bytes 16-24 of a PNG)."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("entry.png: missing IHDR chunk")
    return struct.unpack(">II", data[16:24])


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    with open(SRC, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_SIGNATURE):
        print("entry.png: bad PNG signature", file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print("entry.png: over 1 MiB", file=sys.stderr)
        return 1
    try:
        size = png_dimensions(data)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if size != EXPECTED_SIZE:
        print(f"entry.png: {size[0]}x{size[1]}, expected 1024x1024",
              file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
