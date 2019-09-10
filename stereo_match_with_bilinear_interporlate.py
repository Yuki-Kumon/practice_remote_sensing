# -*- coding: utf-8 -*-

"""
ディープマッチングによるステレオマッチに際し、バイリニア補間を用いる。
Author :
    Yuki Kumon
Last Update :
    2019-09-10
"""


from deepmatch import deepmatch
from tif_to_png import tif_to_png

import os


class stereo_match_with_bilinear_interporlate():
    '''
    stereo matching
    '''

    def __init__(self, img1_path, img2_path):
        if not os.path.exists(img1_path):
            print('img1 path \'{}\' does not exist!'.format(img1_path))
        if not os.path.exists(img2_path):
            print('img2 path \'{}\' does not exist!'.format(img2_path))


if __name__ == '__main__':
    img1 = '/Users/yuki_kumon/Documents/python/practice_remote_sensing/data/band3s.tif'
    img2 = '/Users/yuki_kumon/Documents/python/practice_remote_sensing/data/band3bs.tif'

    cut = [0, 200, 0, 200]
    a = tif_to_png(img1, cut)
    a.create_tmp()

    b = tif_to_png(img2, cut)
    b.create_tmp()

    cls = stereo_match_with_bilinear_interporlate(a(), b())
