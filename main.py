# coolest-art-01: "The Storm Stallion" (v4 candidate).
#
# The entry is a single vendored PNG that this program places at the
# harness output path. Nothing is generated at run time, nothing is
# fetched, and the bytes never change, so any two runs are identical.
# Before copying, the source file is hashed and compared against the
# fingerprint recorded below; a single changed byte aborts the run.
# After copying, the destination is read back and compared byte for
# byte with the source, so a truncated or corrupted write is caught
# instead of silently submitted.
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "c682645476b9d02ebc0a6358e2d722822950877862a5052f4b4895c581defc2e"
IMAGE_NAME = "entry.png"


def _digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _fail(message):
    print("storm-stallion: %s" % message, file=sys.stderr)
    sys.exit(1)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(base, IMAGE_NAME)
    if not os.path.exists(source):
        _fail("vendored image %s is missing next to main.py" % IMAGE_NAME)
    if _digest(source) != EXPECTED_SHA256:
        _fail("vendored image failed its sha256 check")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, IMAGE_NAME)
    shutil.copyfile(source, target)
    if _digest(target) != EXPECTED_SHA256:
        _fail("written image does not match the vendored image")
    size = os.path.getsize(target)
    print("storm-stallion: wrote %s (%d bytes, sha256 ok)" % (target, size))


if __name__ == "__main__":
    main()
