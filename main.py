# main.py — entrypoint for news-image-20261122 (R3).
# Copies entry.png sitting next to this file into MAKEFUN_OUTPUT_DIR
# (default /output) as entry.png. Python 3 stdlib only, no network.
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("main.py: entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
