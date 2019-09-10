# -*- coding: utf-8 -*-

"""
適当な画像でdeepmatchを試す。
Author :
    Yuki Kumon
Last Update :
    2019-07-29
"""

from deepmatch import deepmatch
from tif_to_png import tif_to_png

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2


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
# print(res)

# plot

plt.subplot(1, 2, 1)
im = cv2.imread(a())
plt.imshow(im)
plt.scatter(x=res[:, 0], y=res[:, 1], c=res[:, 4], cmap=cm.Accent)

plt.subplot(1, 2, 2)
im = cv2.imread(b())
plt.imshow(im)
plt.scatter(x=res[:, 2], y=res[:, 3], c=res[:, 4], cmap=cm.Accent)

plt.show()
