#!/usr/bin/env python3
"""Quick test script: create dummy images for multiple plates and verify GIFs.

Run from repo root:
    python tests/run_gif_loop_test.py

No network or Firebase needed — only tests the local GIF creation path.
"""
import os
import shutil
import tempfile
from datetime import datetime

import sys
from PIL import Image
import PIL.ImageFont as ImageFont

# Ensure repo root is on sys.path so imports work when running the test script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Debug: show path info (helpful if import fails)
print(f"[test] ROOT={ROOT}")
print(f"[test] sys.path[0]={sys.path[0]}")
print(f"[test] sys.path contains ROOT? {ROOT in sys.path}")

# Dynamic import by file path — avoids package/import issues when running as script
import importlib.util
gif_module_path = os.path.join(ROOT, "image_processing", "create_gif_from_images.py")
spec = importlib.util.spec_from_file_location("create_gif_from_images", gif_module_path)
gif_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gif_mod)
create_gif_from_images = gif_mod.create_gif_from_images


def ensure_font():
    # Some systems may not have DejaVuSans; fall back to default font
    try:
        ImageFont.truetype("DejaVuSans.ttf", 12)
    except Exception:
        # don't monkeypatch ImageFont.truetype (may cause recursion). We'll let
        # create_gif_from_images fall back to ImageFont.load_default() itself.
        pass


def create_dummy_images(folder, count=6):
    os.makedirs(folder, exist_ok=True)
    for i in range(count):
        img = Image.new("RGB", (320, 240), (i * 30 % 255, i * 50 % 255, i * 70 % 255))
        # include a timestamp-like suffix (no underscores) so the GIF parser can extract it
        ts = datetime.now().strftime("%Y-%m-%dT%H%M%S.%f")
        name = f"img_{ts}.jpg"
        img.save(os.path.join(folder, name))


def main():
    ensure_font()

    tmp = tempfile.mkdtemp(prefix="spore_test_")
    try:
        chamber = "TEST-CHAMBER"
        plates = ["TEST-P1", "TEST-P2"]

        # Create captured_images/<chamber>/<plate> with dummy images
        for plate in plates:
            folder = os.path.join(tmp, "captured_images", chamber, plate)
            create_dummy_images(folder)

        # Run GIF creation for each plate
        success = True
        for plate in plates:
            input_folder = os.path.join(tmp, "captured_images", chamber, plate)
            out_gif_name = f"{plate}.gif"
            print(f"Creating GIF for {plate} from {input_folder} ...")
            create_gif_from_images(input_folder, out_gif_name, 200, 0.1, 1)

            # create_gif_from_images writes GIF into:
            # os.path.join(input_parent_folder, "..", "output_gif_folder")
            input_parent = os.path.dirname(input_folder)
            output_folder = os.path.normpath(os.path.join(input_parent, "..", "output_gif_folder"))
            expected = os.path.join(output_folder, out_gif_name)
            if os.path.exists(expected):
                print(f"OK: found GIF {expected}")
            else:
                print(f"FAIL: GIF not found at {expected}")
                success = False

        if success:
            print("\nAll GIFs created successfully.")
            return 0
        else:
            print("\nOne or more GIFs were not created.")
            return 2

    finally:
        # Cleanup temporary folder
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
