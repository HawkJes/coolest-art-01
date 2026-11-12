# coolest-art-01: the moon-eye entry.
# The program copies the vendored image to the output path, byte for byte,
# then reads the copy back and refuses to finish unless it matches the
# source exactly, including a sha256 check of the vendored file. Standard
# library only; no network. Deterministic: two runs write the same bytes,
# because the file copied never changes.
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "ad002bac87b9748c8eb8bca7488c2d5a99cb4f9ab284a44d92b0e7e74a095c4e"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        want = f.read()
    if hashlib.sha256(want).hexdigest() != EXPECTED_SHA256:
        print("entry.png sha256 mismatch", file=sys.stderr)
        sys.exit(1)
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        got = f.read()
    if got != want:
        print("entry.png copy mismatch", file=sys.stderr)
        sys.exit(1)
    print("wrote %s (%d bytes)" % (dst, len(got)))


if __name__ == "__main__":
    main()
