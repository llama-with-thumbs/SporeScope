#!/usr/bin/env python3
"""Create a dummy GIF and upload it via `firebase_io.upload_gif_file`.

Usage (dry-run):
  python tests/upload_gif_test.py --dry-run --chamber TEST-CH --plate TEST-P1

Usage (real upload):
  python tests/upload_gif_test.py --chamber CHA-8BEA5D1 --plate SMP-9414B8

Be careful: real upload requires `firebase-adminsdk.json` credentials and network access.
"""
import os
import sys
import tempfile
import argparse
from PIL import Image

# Ensure repo root is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from firebase_io.upload_gif_file import upload_gif_file


def make_dummy_gif(path):
    # create two frames with different colors
    frames = []
    for c in ((200, 50, 50), (50, 200, 50)):
        img = Image.new("RGB", (200, 120), color=c)
        frames.append(img)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=200, loop=0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chamber", default="TEST-CHAMBER", help="Chamber id to use in Firestore/storage path")
    parser.add_argument("--plate", default="TEST-PLATE", help="Plate id to use as document id")
    parser.add_argument("--dry-run", action="store_true", help="Do not perform actual upload; just create GIF and show path")
    args = parser.parse_args()

    tmpdir = tempfile.mkdtemp(prefix="upload_gif_test_")
    try:
        gif_path = os.path.join(tmpdir, f"{args.plate}.gif")
        make_dummy_gif(gif_path)
        print(f"Created dummy GIF: {gif_path}")

        if args.dry_run:
            print("Dry-run: skipping upload. Use without --dry-run to perform actual upload.")
            return 0

        print("Uploading to Firebase...")
        upload_gif_file(gif_path, args.chamber, args.plate)
        print("Upload call completed.")
        return 0

    finally:
        # keep temporary for inspection if dry-run was used; otherwise remove
        try:
            import shutil
            shutil.rmtree(tmpdir)
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
