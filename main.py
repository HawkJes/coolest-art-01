# coolest-art-01: the coolest art entry.
# The program copies the vendored image to the output path, byte for byte,
# then reads both files back and refuses to finish unless the copy matches
# the source exactly. Standard library only; no network. Deterministic:
# two runs write the same bytes, because the file copied never changes.
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(src, "rb") as f:
        want = f.read()
    with open(dst, "rb") as f:
        got = f.read()
    if got != want:
        print("entry.png copy mismatch", file=sys.stderr)
        sys.exit(1)
    print("wrote %s (%d bytes)" % (dst, len(got)))


if __name__ == "__main__":
    main()
