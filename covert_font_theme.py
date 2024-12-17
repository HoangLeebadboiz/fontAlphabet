import argparse
import os
import random

import numpy as np
from PIL import Image, ImageFilter

# dataset_path = "dataset1"
# base_dir = "dataset2"


def process_img(img: Image):
    # Convert to numpy
    img_array = np.array(img)
    #  Invert foregound
    img_array[:, :, 0:3] = (
        np.random.randint(140, 220, size=(img_array.shape[0], img_array.shape[1], 3))
        - img_array[:, :, 0:3]
    )
    # Opacity
    # img_array[:, :, 3] = img_array[:, :, 3] * 0.7
    print(img_array[:, :, 3])
    img = Image.fromarray(img_array)
    # Blur image
    # img = img.filter(ImageFilter.GaussianBlur(radius=1))
    return img


def arg_parser():
    parser = argparse.ArgumentParser(
        description="Generate another foreground data for training"
    )
    parser.add_argument(
        "--base-dir",
        type=str,
        default=os.path.join(".", "dataset1"),
        help="Path to the main directory containing character folders",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default=os.path.join(".", "dataset2"),
        help="Path to the output directory",
    )
    return parser.parse_args()


def main():
    args = arg_parser()
    base_dir = args.base_dir
    out_dir = args.out_dir

    # create alphabet list
    alphabet = list("abcdefghijklmnopqrstuvwxyz".upper())
    number = list("0123456789")

    # create folders for each character
    for char in alphabet:
        if not os.path.exists(os.path.join(out_dir, char)):
            os.makedirs(os.path.join(out_dir, char))

    # Create folders for each number
    for num in number:
        if not os.path.exists(os.path.join(out_dir, num)):
            os.makedirs(os.path.join(out_dir, num))

    char_list = os.listdir(base_dir)
    for char in char_list:
        if char == "I":
            continue
        char_file = os.path.join(base_dir, char, char + ".png")
        # char_files = os.listdir(char_path)
        img = Image.open(char_file)
        img = process_img(img)
        img.save(os.path.join(out_dir, char, char + ".png"))


if __name__ == "__main__":
    main()
