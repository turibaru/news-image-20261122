"""News-image entry for make.fun (news-image-20261122).

The entry is a single newspaper front page, ``entry.png`` (1024x1024),
sitting next to this file. Running this program copies that image to the
output directory, after checking it is a valid PNG inside the gate limits
(at most 1 MiB, at most 1024x1024). The judge receives exactly the bytes
copied here, so the copy is verified byte-for-byte with SHA-256 before the
program reports success. No network, no randomness: every run produces the
same bytes.

Usage (outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output):

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Without MAKEFUN_OUTPUT_DIR the image goes to /output/entry.png.
"""

import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def fail(message):
    print(f"main.py: error: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SRC):
        fail(f"bundled image not found: {SRC}")

    with open(SRC, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        fail("bundled entry.png is not a PNG file")

    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        fail(f"bundled entry.png is {size} bytes, over the 1 MiB gate limit")

    # The PNG header is 33 bytes: 8 signature bytes plus the 25-byte IHDR
    # chunk header. Inside it, the chunk type sits at bytes 12-15, the
    # width at bytes 16-19 and the height at bytes 20-23, both big-endian.
    with open(SRC, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[12:16] != b"IHDR":
        fail("bundled entry.png has no IHDR chunk")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if width > 1024 or height > 1024:
        fail(f"bundled entry.png is {width}x{height}, over the 1024x1024 gate limit")

    source_hash = sha256_of(SRC)

    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, dest)

    if os.path.getsize(dest) != size:
        fail("copied entry.png does not match the bundled file size")
    if sha256_of(dest) != source_hash:
        fail("copied entry.png does not match the bundled file byte-for-byte")

    print(f"wrote {dest} ({size} bytes, sha256 {source_hash})")


if __name__ == "__main__":
    main()
