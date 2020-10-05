# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("/usr/local/lib/python3.8/site-packages")
import argparse
from PIL import Image
from PIL import ImageOps
from PIL import ImageFilter
from PIL import ImageEnhance
from cv2 import bilateralFilter
import numpy as np

def cut_padding(img):
    np_img = np.array(img)
    all_white_val = 255 * img.size[0]

    col_sum = [np.sum(np_img[:,i]) for i in range(img.size[0])]
    col_idx = np.where(np.array(col_sum) < all_white_val)
    col_from, col_to = col_idx[0][0], col_idx[0][-1]

    row_sum = [np.sum(np_img[i,:]) for i in range(img.size[1])]
    row_idx = np.where(np.array(row_sum) < all_white_val)
    row_from, row_to = row_idx[0][0], row_idx[0][-1]

    return img.crop((col_from, row_from, col_to + 1, row_to + 1))


def add_padding(img, size = 2, color=(255)):
    return ImageOps.expand(img, size, color)


def crop_image_uniform(src_dir, dst_dir):
    f = open("399-uniform.txt", "r")
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for page in range(1,4):
        img = Image.open( src_dir + "/" + str(page) +"-uniform.png").convert('L')
        img = cut_padding(img)

        width, height = img.size
        cell_width = width/float(cols)
        cell_height = height/float(rows)
        header_offset = height/float(rows) * header_ratio
        width_margin = cell_width * 0.10
        height_margin = cell_height * 0.10

        for j in range(0,rows):
            for i in range(0,cols):
                left = i * cell_width
                upper = j * cell_height + header_offset
                right = left + cell_width
                lower = (j+1) * cell_height

                center_x = (left + right) / 2
                center_y = (upper + lower) / 2

                crop_width = right - left - 2*width_margin
                crop_height = lower - upper - 2*height_margin

                size = 0
                if crop_width > crop_height:
                    size = crop_height/2
                else:
                    size = crop_width/2

                left = center_x - size
                right = center_x + size
                upper = center_y - size
                lower = center_y + size

                code = f.readline()
                if not code:
                    break
                else:
                    name = dst_dir + "/uni" + code.strip() + ".png"
                    cropped_image = img.crop((left, upper, right, lower))
                    cropped_image = cropped_image.resize((128,128), Image.LANCZOS)
                    # Increase constrast
                    enhancer = ImageEnhance.Contrast(cropped_image)
                    cropped_image = enhancer.enhance(1.5)
                    opencv_image = np.array(cropped_image)
                    opencv_image = bilateralFilter(opencv_image, 9, 30, 30)
                    cropped_image = Image.fromarray(opencv_image)

                    no_padding = cut_padding(cropped_image).resize((60,60))
                    padding = add_padding(no_padding, 34)

                    padding.save(name)
        print("Processed uniform page " + str(page))

parser = argparse.ArgumentParser(description='Crop scanned images to character images')
# parser.add_argument('--src_dir', dest='src_dir', required=True, help='directory to read scanned images')
# parser.add_argument('--dst_dir', dest='dst_dir', required=True, help='directory to save character images')

args = parser.parse_args()

if __name__ == "__main__":
    rows = 12
    cols = 12
    header_ratio = 16.5/(16.5+42)
    #crop_image_uniform(args.src_dir, args.dst_dir)
    crop_image_uniform(".", "./img3")
    #crop_image_frequency(args.src_dir, args.dst_dir)
