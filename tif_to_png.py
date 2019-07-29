# -*- coding: utf-8 -*-

"""
tifファイルをpngに変換してdeepmatchのコードに入れられるようにする。
Author :
    Yuki Kumon
Last Update :
    2019-07-29
"""

import cv2
import sys
import os


class tif_to_png():
    '''
    tifからpngに変換。
    '''

    def __init__(self, path, cut=None):
        '''
        cutは[xmin, xmax, ymin, ymax] = [0, 100, 0, 200]のようなリストで代入
        '''
        self.path = ''
        self.savepath = ''
        self.cut = cut
        if self.is_exit(path):
            self.path = path

    def is_exit(self, path):
        if not os.path.exists(path):
            print('invalid path!: {}'.format(path))
            return False
        else:
            return True

    def cutter(self, img):
        cut = self.cut
        return img[cut[2]: cut[3], cut[0]:cut[1]]

    def create_tmp(self):
        '''
        tmpファイルを作成。
        '''
        # load
        img = cv2.imread(self.path)

        # create tmp file
        self.savepath = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(self.path))[0] + '.png')
        if self.cut:
            cv2.imwrite(self.savepath, self.cutter(img))
        else:
            cv2.imwrite(self.savepath, img)
        self.is_exit(self.savepath)

    def __call__(self):
        return self.savepath

    def __del__(self):
        if self.is_exit(self.savepath):
            os.remove(self.savepath)
