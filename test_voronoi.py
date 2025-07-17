"""
Image Folder Comparison Tool

This script compares PNG image files between two directory structures to check for exact pixel-level matches.
Useful for validating image data integrity after preprocessing, augmentation, or generation pipelines.

Usage (command line):
$ python compare_images.py /path/to/base /path/to/test 
$ python test_voronoi.py /path/to/base /path/to/test --subfolders train/images valid/images

Arguments:
- base_path: Path to the reference (base) folder
- test_path: Path to the folder to compare against
- --subfolders: List of subfolder paths to compare (default: train/images, valid/images, train/labels, valid/labels)
"""


import os
from PIL import Image
import numpy as np
import sys
import argparse

def compare_images(img1_path, img2_path):
    try:
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(img2_path).convert('RGB')
        return np.array_equal(np.array(img1), np.array(img2))
    except Exception as e:
        print(f"Error comparing {img1_path} and {img2_path}: {e}")
        return False

def compare_image_folders(base_root, test_root, subfolders=["train/images", "valid/images", "train/labels", "valid/labels"]):
    # Check if root directories exist
    if not os.path.exists(base_root):
        sys.exit(f"❌ Base folder does not exist: {base_root}")
    if not os.path.exists(test_root):
        sys.exit(f"❌ Test folder does not exist: {test_root}")

    mismatches = []
    checked_files = 0

    for subfolder in subfolders:
        base_dir = os.path.join(base_root, subfolder)
        test_dir = os.path.join(test_root, subfolder)

        if not os.path.exists(base_dir):
            print(f"⚠️ Subfolder not found in base: {base_dir}")
            continue
        if not os.path.exists(test_dir):
            print(f"⚠️ Subfolder not found in test: {test_dir}")
            continue

        base_images = sorted([f for f in os.listdir(base_dir) if f.endswith('.png')])
        test_images = sorted([f for f in os.listdir(test_dir) if f.endswith('.png')])

        # Warn if file lists do not match
        if base_images != test_images:
            print(f"⚠️ File list mismatch in: {subfolder}")
            base_set = set(base_images)
            test_set = set(test_images)
            print("  - Only in base:", base_set - test_set)
            print("  - Only in test:", test_set - base_set)

        # Compare only common files
        common_images = set(base_images) & set(test_images)
        for img_name in sorted(common_images):
            base_img_path = os.path.join(base_dir, img_name)
            test_img_path = os.path.join(test_dir, img_name)

            if not compare_images(base_img_path, test_img_path):
                mismatches.append((subfolder, img_name, "Content mismatch"))
            else:
                checked_files += 1

    # Summary
    print(f"\n🔍 Total images checked: {checked_files}")
    if mismatches:
        print("❌ Mismatches found:")
        # for subfolder, img_name, reason in mismatches:
        #     print(f" - {subfolder}/{img_name}: {reason}")
    else:
        print("✅ All images match!")

# Entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare image folders')
    parser.add_argument('base_path', help='Path to the base folder')
    parser.add_argument('test_path', help='Path to the test folder')
    parser.add_argument('--subfolders', nargs='+', 
                        default=["train/images", "valid/images", "train/labels", "valid/labels"],
                        help='Subfolders to compare (default: train/images valid/images train/labels valid/labels)')
    
    args = parser.parse_args()
    
    compare_image_folders(args.base_path, args.test_path, args.subfolders)
