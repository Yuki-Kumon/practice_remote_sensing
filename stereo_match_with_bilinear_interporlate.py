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


if __name__ == '__main__':
    img1 = '/Users/yuki_kumon/Documents/python/practice_remote_sensing/data/band3s.tif'
    img2 = '/Users/yuki_kumon/Documents/python/practice_remote_sensing/data/band3bs.tif'

    cut = [0, 200, 0, 200]
    a = tif_to_png(img1, cut)
    a.create_tmp()

    b = tif_to_png(img2, cut)
    b.create_tmp()

    # res = deepmatch(img1, img2, nt=0)
    res = deepmatch(a(), b(), max_scale=1, nt=2)
    print(res)
    print(len(res))
