# -*- coding: utf-8 -*-

"""
ディープマッチングによるステレオマッチに際し、バイリニア補間(cv2.resize())を用いる。
Author :
    Yuki Kumon
Last Update :
    2019-09-10
"""


from deepmatch import deepmatch
from tif_to_png import tif_to_png

import cv2
import numpy as np
import pandas as pd

import os
import sys


class stereo_match_with_bilinear_interpolate():
    '''
    stereo matching
    '''

    def __init__(self, img1_path, img2_path, cut_start=[0, 0], cut_size=[200, 200], cut_number=[1, 1]):
        '''
        input image: tif or png
        '''
        # sanity check
        if not os.path.exists(img1_path):
            print('img1 path \'{}\' does not exist!'.format(img1_path))
            sys.exit()
        if not os.path.exists(img2_path):
            print('img2 path \'{}\' does not exist!'.format(img2_path))
            sys.exit()

        if os.path.splitext(img1_path)[1] != '.png' and os.path.splitext(img1_path)[1] != '.tif':
            print('img1 path extension \'{}\' is not supported. tif or png is ok.'.format(os.path.splitext(img1_path)[1]))
            sys.exit()
        if os.path.splitext(img2_path)[1] != '.png' and os.path.splitext(img2_path)[1] != '.tif':
            print('img2 path extension \'{}\' is not supported. tif or png is ok.'.format(os.path.splitext(img2_path)[1]))
            sys.exit()

        self.img1_path = img1_path
        self.img2_path = img2_path
        self.cut_start = cut_start
        self.cut_size = cut_size
        self.cut_number = cut_number

    def deepmatching(self):
        '''
        deepmatching
        '''
        result_array = 0  # dummy
        for i in range(self.cut_number[0]):
            for j in range(self.cut_number[1]):
                cut = [
                    self.cut_start[0] + self.cut_size[0] * i, self.cut_start[0] + self.cut_size[0] * (i + 1),
                    self.cut_start[1] + self.cut_size[1] * j, self.cut_start[1] + self.cut_size[1] * (j + 1)
                ]
                # create tmp images
                img1_cut = tif_to_png(self.img1_path, cut)
                img1_cut.create_tmp()
                img2_cut = tif_to_png(self.img2_path, cut)
                img2_cut.create_tmp()

                """
                # DeepMatching
                res = deepmatch(img1_cut(), img2_cut(), max_scale=1, nt=2)
                # 視差を計算した上で格子状にソートした結果を受け取る。後で二次関数近似とかを使えると嬉しいので相関値も。
                res_d_sort = self.res_sort(res)

                # 配列に格納
                if i == 0 and j == 0:
                    result_array = np.empty((self.cut_number[0], self.cut_number[1], res_d_sort.shape[0], res_d_sort.shape[1]))
                    result_array[0, 0] = res_d_sort
                else:
                    result_array[i, j] = res_d_sort
                """
                result_array = self.deepmatching_update(cut, img1_cut, img2_cut, result_array, i, j)
        return result_array

    def deepmatching_update(self, cut, tmp1, tmp2, result_array, i, j):
        '''
        たまに変なサイズで帰ってくることがあるのでそれ対策
        一番初めが妙なサイズだと対応できない。。。
        '''
        while True:
            # DeepMatching
            res = deepmatch(tmp1(), tmp2(), max_scale=1, nt=2)
            # 視差を計算した上で格子状にソートした結果を受け取る。後で二次関数近似とかを使えると嬉しいので相関値も。
            res_d_sort = self.res_sort(res)
            # 配列に格納
            if i == 0 and j == 0:
                del result_array
                result_array = np.empty((self.cut_number[0], self.cut_number[1], res_d_sort.shape[0], res_d_sort.shape[1]))
                result_array[0, 0] = res_d_sort
                break
            else:
                try:
                    result_array[i, j] = res_d_sort
                    break
                except:
                    print('error occurs')
        return result_array

    def res_sort(self, res):
        '''
        deepmatchingの返り値をソートする
        '''
        # resを整形
        res_d = np.empty((res.shape[0], 4))
        res_d[:, :2] = res[:, :2]
        res_d[:, 2] = res[:, 0] - res[:, 2]  # 視差
        res_d[:, 3] = res[:, 4]  # 相関値
        # ソートする(pandas利用)
        df = pd.DataFrame(data=res_d, columns=['x', 'y', 'd', 'R'])
        df = df.sort_values(['x', 'y'])
        # numpyに戻してreturnする
        return df.values

    def res_interpolate(self, result_array):
        '''
        deepmatchingの結果を補完し、視差画像にする
        '''
        # result arrayのうち、相関値は使わずに行う
        d_array = result_array[:, :, :, :3].astype('int64')
        # 整形後の配列のサイズを計算しておく
        x_min = d_array[0, 0, 0, 0]
        y_min = d_array[0, 0, 0, 1]
        x_max = d_array[0, 0, -1, 0]
        y_max = d_array[0, 0, -1, 1]

        x_num = int((x_max - x_min) / 8)
        y_num = int((y_max - y_min) / 8)

        # タイル状に並べ換える
        return 0

    def __call__(self):
        '''
        deepmatchingによるステレオマッチング
        '''
        result_array = self.deepmatching()
        hoge = self.res_interpolate(result_array)




if __name__ == '__main__':
    img1 = '/Users/yuki_kumon/Documents/python/practice_remote_sensing/data/band3s.tif'
    img2 = '/Users/yuki_kumon/Documents/python/practice_remote_sensing/data/band3bs.tif'

    cut = [0, 200, 0, 200]
    a = tif_to_png(img1, cut)
    a.create_tmp()

    b = tif_to_png(img2, cut)
    b.create_tmp()

    cls = stereo_match_with_bilinear_interpolate(a(), b())
    cls()
