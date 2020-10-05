#-*- coding: utf-8 -*-

import sys, os, time
sys.path.append("/usr/local/lib/python3.8/site-packages")
import numpy as np
from PIL import Image, ImageOps
import pickle
import random

src_path = "./hangul3/"

def cut_padding(img):
    np_img = np.array(img)
    all_white_val = 255 * img.size[0]
    col_sum = [np.sum(np_img[:,i]) for i in range(img.size[1])]
    col_idx = np.where(np.array(col_sum) < all_white_val)
    col_from, col_to = col_idx[0][0], col_idx[0][-1]

    row_sum = [np.sum(np_img[i,:]) for i in range(img.size[0])]
    row_idx = np.where(np.array(row_sum) < all_white_val)
    row_from, row_to = row_idx[0][0], row_idx[0][-1]

    return img.crop((col_from, row_from, col_to + 1, row_to + 1))


def add_padding(img, size = 2, color=(255)):
    return ImageOps.expand(img, size, color)


def make_clear(img):
    np_img = np.array(img)
    np_img = np.where(np_img > 200, 255, np_img)
    return Image.fromarray(np_img)


def text2img(text):
    back_color = 255
    board_width = 800
    board_height = 800
    h_margin = 40
    v_margin = 40

    r_offset = v_margin
    c_offset = h_margin

    font_width = 8
    font_height = 8

    gap = 3
    h_gap = 12
    v_gap = 24
    file_name = "tmp.png"
    board = np.ones((board_height, board_width)) * back_color

    for c in text:
        font_width = 16 + random.randrange(0, 7)
        font_height = 20 + random.randrange(0, 7)

        if c == " ":
            c_offset += h_gap + random.randrange(0, 7)
        elif c == "\n":
            r_offset += (font_height + v_gap)
            c_offset = h_margin
        else:
            img = Image.open(src_path + c + ".png").resize((128,128)).convert("L")
            img = make_clear(img)
            img = cut_padding(img).resize((font_width,font_height))
            img = np.array(img)
            board[r_offset:r_offset+font_height, c_offset:c_offset+font_width] = img
            c_offset += (font_width+gap)
        if c_offset+font_width > board_width-h_margin:
            c_offset = h_margin
            r_offset += (font_height + v_gap)
        if r_offset+font_height > board_height-v_margin:
            break

    res = Image.fromarray(board.astype(np.uint8))
    res.save(file_name)
    return file_name