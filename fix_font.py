import os

from PIL import Image

char_path = "dataset1/Q/2186.png"
img = Image.open(char_path)
img = img.resize((int(img.width * 2), int(img.height * 2)))
print(img.width, img.height)
img.save("./2186.png")
