import argparse
import json
import math
import os
import random

import cv2
import numpy as np
from PIL import Image, ImageFilter

# Path to the main directory containing character folders
base_dir = os.path.join(".", "dataset1")

# Path to the background image
background_image_path = os.path.join(".", "background", "background1.png")


def registry_chars(base_dir):
    char_registry = {
        "0": (os.path.join(base_dir, "0", "0.png"), 0),
        "1": (os.path.join(base_dir, "1", "1.png"), 1),
        "2": (os.path.join(base_dir, "2", "2.png"), 2),
        "3": (os.path.join(base_dir, "3", "3.png"), 3),
        "4": (os.path.join(base_dir, "4", "4.png"), 4),
        "5": (os.path.join(base_dir, "5", "5.png"), 5),
        "6": (os.path.join(base_dir, "6", "6.png"), 6),
        "7": (os.path.join(base_dir, "7", "7.png"), 7),
        "8": (os.path.join(base_dir, "8", "8.png"), 8),
        "9": (os.path.join(base_dir, "9", "9.png"), 9),
        "A": (os.path.join(base_dir, "A", "A.png"), 10),
        "B": (os.path.join(base_dir, "B", "B.png"), 11),
        "C": (os.path.join(base_dir, "C", "C.png"), 12),
        "D": (os.path.join(base_dir, "D", "D.png"), 13),
        "E": (os.path.join(base_dir, "E", "E.png"), 14),
        "F": (os.path.join(base_dir, "F", "F.png"), 15),
        "G": (os.path.join(base_dir, "G", "G.png"), 16),
        "H": (os.path.join(base_dir, "H", "H.png"), 17),
        # "I": (os.path.join(base_dir, "I", "I.png"), 18),
        "J": (os.path.join(base_dir, "J", "J.png"), 19),
        "K": (os.path.join(base_dir, "K", "K.png"), 20),
        "L": (os.path.join(base_dir, "L", "L.png"), 21),
        "M": (os.path.join(base_dir, "M", "M.png"), 22),
        "N": (os.path.join(base_dir, "N", "N.png"), 23),
        "O": (os.path.join(base_dir, "O", "O.png"), 24),
        "P": (os.path.join(base_dir, "P", "P.png"), 25),
        # "Q": (os.path.join(base_dir, "Q", "Q.png"), 26),
        "R": (os.path.join(base_dir, "R", "R.png"), 27),
        "S": (os.path.join(base_dir, "S", "S.png"), 28),
        "T": (os.path.join(base_dir, "T", "T.png"), 29),
        "U": (os.path.join(base_dir, "U", "U.png"), 30),
        "V": (os.path.join(base_dir, "V", "V.png"), 31),
        "W": (os.path.join(base_dir, "W", "W.png"), 32),
        "X": (os.path.join(base_dir, "X", "X.png"), 33),
        "Y": (os.path.join(base_dir, "Y", "Y.png"), 34),
        "Z": (os.path.join(base_dir, "Z", "Z.png"), 35),
        # ":": (os.path.join(base_dir, "Colon"), 36),
        # "/": (os.path.join(base_dir, "Slash"), 37),
    }
    return char_registry


def put_img_on_background(char_img: Image.Image, bg_img, position):
    bg_img.paste(
        char_img, position, char_img.convert("RGBA")
    )  # Use RGBA for transparency support


def generate_string():
    numbers = "0123456789"
    chars = "ABCDEFGHJKLMNOPRSTUVWXYZ"
    sentence = (
        "".join(random.choices(numbers, k=3))
        + "".join(random.choices(chars, k=3))
        + "".join(random.choices(numbers, k=1))
        + "".join(random.choices(chars, k=2))
        + "".join(random.choices(numbers, k=1))
    )
    return sentence


def analyze_sentence(sentence, char_registry):
    chars = list(sentence)
    char_list = list()
    for char in chars:
        if char in char_registry:
            char_list.append((char.lower(), char_registry[char][0]))
        else:
            print(f"Character {char} not found in the registry")
    return char_list


def process_char_img(char_path):
    char_img = Image.open(char_path)
    char_img = char_img.convert("RGBA")
    if char_path.endswith("M.png") or char_path.endswith("W.png"):
        char_img = char_img.resize((23, 25))
    else:
        char_img = char_img.resize((15, 25))
    char_img_array = np.array(char_img)
    char_img_array[:, :, 3] = char_img_array[:, :, 3] * random.uniform(0.7, 0.8)
    char_img = Image.fromarray(char_img_array, "RGBA")
    char_img = char_img.filter(ImageFilter.GaussianBlur(radius=0.5))
    return char_img


def args_parser():
    parser = argparse.ArgumentParser(description="Generate data for training")
    parser.add_argument(
        "--base-dir",
        type=str,
        default=os.path.join(".", "dataset1"),
        help="Path to the main directory containing character folders",
    )
    parser.add_argument(
        "--background-image-path",
        type=str,
        default=os.path.join(".", "background", "background1.png"),
        help="Path to the background image",
    )
    parser.add_argument(
        "--save-dir", type=str, default="./output", help="Path to save the image"
    )
    parser.add_argument(
        "--num-images", type=int, default=100, help="Number of images generated"
    )
    return parser.parse_args()


def main():
    args = args_parser()
    base_dir = args.base_dir
    background_image_path = args.background_image_path
    save_dir = args.save_dir
    if os.path.exists(save_dir) == False:
        os.makedirs(save_dir)
    if os.path.exists(os.path.join(save_dir, "images")) == False:
        os.makedirs(os.path.join(save_dir, "images"))
    if os.path.exists(os.path.join(save_dir, "annotations")) == False:
        os.makedirs(os.path.join(save_dir, "annotations"))
    num_images = args.num_images
    background_name = os.path.basename(background_image_path).split(".")[0]
    char_registry = registry_chars(base_dir)
    images_path = os.path.join(save_dir, "images")
    annotations_path = os.path.join(save_dir, "annotations")
    for i in range(num_images):
        sentence = generate_string()
        char_list = analyze_sentence(sentence, char_registry)
        background = Image.open(background_image_path)
        position = (
            int(background.width / 1.75) + random.randint(-5, 5),
            int(background.height / 2.3) + random.randint(-2, 2),
        )
        center = position
        angle = random.randint(-2, 2)
        annotations_list = list()
        for char, char_path in char_list:
            char_img = process_char_img(char_path)
            char_img_new, position_new = random_rotate(
                center, char_img, position, angle
            )
            put_img_on_background(char_img_new, background, position_new)
            annotations_list.append(
                {
                    "x": position_new[0],
                    "y": position_new[1],
                    "w": char_img_new.width,
                    "h": char_img_new.height,
                    "annotation": char,
                }
            )
            position = (position[0] + char_img.width + 1, position[1])
        background.save(os.path.join(images_path, f"{background_name}_{i+1}.png"))
        annotations = json.dumps(annotations_list)
        with open(
            os.path.join(annotations_path, f"{background_name}_{i+1}.png.txt"), "w"
        ) as f:
            f.write(f"{annotations}")
            f.close()


def random_rotate(center, img: Image, position, angle):
    rotated_img = img.rotate(angle, expand=True)
    # Update position flowing center
    position = (
        int((position[0] - center[0]) * math.cos(math.radians(angle)) + center[0]),
        int(-(position[0] - center[0]) * math.sin(math.radians(angle)) + center[1]),
    )
    return rotated_img, position


if __name__ == "__main__":
    main()
