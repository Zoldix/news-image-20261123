"""Validasi dan salin sampul koran satu halaman untuk entri
news-image-20261123 (make.fun).

Entri ini adalah koran satu halaman berisi berita dunia
Senin 23 November 2026. Program ini memeriksa file
``entry.png`` di direktori yang sama — memastikan file itu
PNG 1024x1024 yang sah dan di bawah batas ukuran — lalu
menyalinnya ke direktori output yang ditentukan lewat
environment ``MAKEFUN_OUTPUT_DIR`` (default ``/output``).
Program ini hanya memakai pustaka standar Python, tidak
mengakses jaringan, dan deterministik: keluaran selalu
salinan byte-per-byte dari file sumber yang lolos validasi.
"""

import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def fail(message):
    """Cetak pesan error ke stderr dan keluar non-zero."""
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    if not os.path.isfile(source):
        fail(f"entry.png tidak ditemukan di {here}")

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        fail(f"entry.png terlalu besar: {size} byte (maks {MAX_BYTES})")

    with open(source, "rb") as handle:
        header = handle.read(24)

    if len(header) < 24:
        fail("entry.png terlalu pendek untuk header PNG")
    if header[:8] != PNG_SIGNATURE:
        fail("entry.png bukan file PNG (signature tidak cocok)")
    if header[12:16] != b"IHDR":
        fail("entry.png tidak memiliki chunk IHDR yang valid")

    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        fail(
            f"ukuran entry.png {width}x{height}, "
            f"harus {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, destination)

    print(f"entry.png disalin ke {destination} ({size} byte)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
