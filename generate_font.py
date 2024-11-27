import os
import shutil

from PIL import Image

dataroot = "./dataset1"
database = "C:/Users/HoangLee/Desktop/data/training_data"

# create alphabet list
alphabet = list("abcdefghijklmnopqrstuvwxyz".upper())
number = list("0123456789")

for char in alphabet:
    if os.path.exists(os.path.join(dataroot, char)) == False:
        os.makedirs(os.path.join(dataroot, char))

for num in number:
    if os.path.exists(os.path.join(dataroot, num)) == False:
        os.makedirs(os.path.join(dataroot, num))

char_list = os.listdir(dataroot)

begin = 144
for char in char_list:
    # copy file
    char_path = os.path.join(database, char, f"{begin}.png")
    des = os.path.join(dataroot, char, f"{begin}.png")
    shutil.copyfile(src=char_path, dst=des)
    begin += 1

# scale image
ratio = 3
for char in char_list:
    char_path = os.path.join(dataroot, char)
    char_files = os.listdir(char_path)
    for file in char_files:
        img = Image.open(os.path.join(char_path, file))
        img = img.resize((img.width * ratio, img.height * ratio))
        img.save(os.path.join(char_path, file))
