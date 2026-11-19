"""Deliver the 19 November 2026 front page to the output directory.

This repository holds a single picture, entry.png: a newspaper front page
that sums up the world news of Thursday 19 November 2026, drawn up from
that morning's reporting. The page leads with the first trilateral meeting
of the American, Chinese and Russian presidents in Shenzhen, then the
widening war in the Gulf, the worldwide launch of GTA VI, the World Court's
Rohingya genocide verdict, and Cyclone Akvan closing on India's east coast,
with a strip of shorter business and culture stories along the foot.

At run time this program only copies those fixed bytes into place. It
reaches for no network, reads no clock, and rolls no dice, so a second run
writes exactly the same file as the first.
"""

from hashlib import sha256
from os import environ
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PICTURE = ROOT / "entry.png"
MAGIC = b"\x89PNG\r\n\x1a\n"


def fingerprint(path: Path) -> str:
    """Return the hex digest of a file's full contents."""
    return sha256(path.read_bytes()).hexdigest()


def copy_entry() -> int:
    """Copy entry.png to the output folder and prove the copy is whole."""
    destination = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "entry.png"
    target.write_bytes(PICTURE.read_bytes())
    if target.read_bytes()[: len(MAGIC)] != MAGIC:
        print("error: output does not begin with the PNG signature", flush=True)
        return 1
    if fingerprint(target) != fingerprint(PICTURE):
        print("error: output bytes differ from the stored picture", flush=True)
        return 1
    if target.stat().st_size > 1_048_576:
        print("error: output is larger than the 1 MiB limit", flush=True)
        return 1
    print(f"wrote {target} ({target.stat().st_size} bytes)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(copy_entry())
