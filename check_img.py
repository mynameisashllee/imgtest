# Modified from find_similar_images.py (https://github.com/JohannesBuchner/imagehash/blob/master/find_similar_images.py)

import os
from PIL import Image
import imagehash

def setup_problematic_img(hashfunc=imagehash.phash):
    directory = os.fsencode("banana_dataset/banana") # change this to the directory of problematic images
    img_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.svg')
    problematic_img_hashes = []

    for file in os.listdir(directory):
        dir_str = os.fsdecode(directory).lower()
        filename = os.fsdecode(file).lower()
        if filename.endswith(img_formats): 
            try:
                hash = hashfunc(Image.open(dir_str + "\\" + filename)) # might have to remove "\\" if images in same directory
                problematic_img_hashes.append(hash)
            except Exception as e:
                print('Problem:', e, 'with', filename)
                continue
        else:
            continue
    
    return problematic_img_hashes
    
def check_img(problematic_img_hashes, img_path, hashfunc = imagehash.phash): 
    try:
        img = Image.open(img_path)
        hash = hashfunc(img)
    except Exception as e:
        print('Error occured with reading file:', e)
    
    if hash in problematic_img_hashes:
        print("Image is problematic")
    else:
        print("Image is OK") # change this to send the message to the receiver

problematic_img_hashes = setup_problematic_img()
check_img(problematic_img_hashes, "banana_dataset/0CNHV8VNNO2K_rot.jpg") # change img_path with the image received via socket

