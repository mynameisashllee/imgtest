# just checking images

import os
from PIL import Image
import imagehash

def setup_problematic_img(hashfunc=imagehash.phash):
    directory = "problematic"  # directory of problematic images
    img_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.svg')
    problematic_img_hashes = []

    for file in os.listdir(directory):
        filename = os.path.join(directory, file).lower()
        if filename.endswith(img_formats):
            try:
                img_hash = hashfunc(Image.open(filename))
                problematic_img_hashes.append(img_hash)
            except Exception as e:
                print('Problem:', e, 'with', filename)
                continue
    
    return problematic_img_hashes

def check_img(problematic_img_hashes, img_path, hashfunc=imagehash.phash, threshold=5):
    try:
        img = Image.open(img_path)
        img_hash = hashfunc(img)
    except Exception as e:
        print('Error occurred with reading file:', e)
        return
    
    for p_hash in problematic_img_hashes:
        if img_hash - p_hash <= threshold:
            print("Image is problematic")
            return
    
    print("Image is OK")

if __name__ == '__main__':
    problematic_img_hashes = setup_problematic_img()
    check_img(problematic_img_hashes, "applephotos/problemapplemed.jpeg")  # change img_path with the image received via socket
