# -*- coding: utf-8 -*-

"""
Deep Match
http://lear.inrialpes.fr/src/deepmatching/
↑からdeepmatchingのアルゴリズムを拝借
Author :
    Yuki Kumon
Last Update :
    2019-07-22
"""

# from src.deepmatching.deepmatching import deepmatching

# pythonラッパーのコンパイルができなくて無事死亡。。。

import subprocess
import cv2
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import time


ROOT = '/Users/yuki_kumon/Documents/python/practice_remote_sensing/src/deepmatching'


def deepmatch(img1, img2, nt=2):
    '''
    自作pythonラッパー。。。
    '''

    t1 = time.time()

    os.chdir(ROOT)
    cmd = './deepmatching'

    # 画像ファイルが存在するかどうか確認
    if(not (os.path.isfile(img1) and os.path.isfile(img2))):
        print('please set valid image path!')
        pass
    print('image 1 size: {}, image 2 wize: {}'.format(cv2.imread(img1).shape, cv2.imread(img2).shape))

    # deepmatchingを行う
    proc = subprocess.run([cmd, img1, img2, '-nt', str(nt)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    array = proc.stdout.decode("utf8")
    array = array.replace('\n', ' ').split(' ')[:-1]
    array = np.array([float(str) for str in array]).reshape(int(len(array) / 6), 6)

    t2 = time.time()
    print('deepmatching is finished. time: {}'.format(t2 - t1))

    return array


if __name__ == '__main__':
    img1 = '/Users/yuki_kumon/Documents/python/practice_remote_sensing/src/deepmatching/climb1.png'
    img2 = '/Users/yuki_kumon/Documents/python/practice_remote_sensing/src/deepmatching/climb2.png'
    res = deepmatch(img1, img2, nt=0)

    # plot

    plt.subplot(1, 2, 1)
    im = cv2.imread(img1)
    plt.imshow(im)
    plt.scatter(x=res[:, 0], y=res[:, 1], c=res[:, 4], cmap=cm.Accent)

    plt.subplot(1, 2, 2)
    im = cv2.imread(img2)
    plt.imshow(im)
    plt.scatter(x=res[:, 2], y=res[:, 3], c=res[:, 4], cmap=cm.Accent)

    plt.show()
