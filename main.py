# A make.fun news-image entry (Python 3.13, standard library only): the image
# is the entry.png beside this file, and the program copies it to
# /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB and
# 1024 by 1024 pixels, and the judge sees exactly the bytes copied. No
# network, fully deterministic: every run writes the same bytes.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
#
# The bundled image is validated before copying (PNG magic bytes and the
# 1 MiB gate limit) and the copy is verified byte-for-byte afterwards with
# SHA-256, so a corrupt or truncated entry.png fails loudly here instead of
# silently handing the judge a bad file. The bytes written are unchanged.

import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def fail(message):
    print(f"main.py: error: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SRC):
        fail(f"bundled image not found: {SRC}")
    with open(SRC, "rb") as f:
        header = f.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        fail("bundled entry.png is not a PNG file")
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        fail(f"bundled entry.png is {size} bytes, over the 1 MiB gate limit")
    with open(SRC, "rb") as f:
        ihdr = f.read(33)
    if len(ihdr) < 33 or ihdr[12:16] != b"IHDR":
        fail("bundled entry.png has no IHDR chunk")
    width = int.from_bytes(ihdr[16:20], "big")
    height = int.from_bytes(ihdr[20:24], "big")
    if width > 1024 or height > 1024:
        fail(f"bundled entry.png is {width}x{height}, over the 1024x1024 gate limit")
    src_hash = sha256_of(SRC)

    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, dest)
    if os.path.getsize(dest) != size:
        fail("copied entry.png does not match the bundled file size")
    if sha256_of(dest) != src_hash:
        fail("copied entry.png does not match the bundled file byte-for-byte")
    print(f"wrote {dest} ({size} bytes, sha256 {src_hash})")


if __name__ == "__main__":
    main()
