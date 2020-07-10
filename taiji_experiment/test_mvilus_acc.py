# -*- coding:utf-8 -*-
# @author :adolf
import os
from PIL import Image
import matplotlib.pyplot as plt

from feature_experiment.test_api import *

img_file_path = "/home/shizai/datadisk5/cv/image_retrieval/taiji_test/"
img_list = os.listdir(img_file_path)

img_id = 6267
img_name = img_list[img_id]
# print(img_name)
file_path = os.path.join(img_file_path, img_name)
fileid = "taiji_test_" + str(img_id)
file_base64 = path2base64(file_path)
result = getSimilarImages_str(fileid, file_base64)
# print('1111', result)
result = result.replace('[', '').replace(']', '').replace("'", '').replace(' ', '')
result = result.split(',')[1:]
# print(result)

# img_q = Image.open(file_path)
# plt.imshow(img_q)
# plt.show()

flag = 0
for rank_img_name in result:
    print(rank_img_name)
    if "taiji_test" not in rank_img_name or flag > 10:
        continue
    img_index = rank_img_name.split('_')[-1]
    rank_img_path = os.path.join(img_file_path, img_list[int(img_index)])
    # print(rank_img_path)
    img_r = Image.open(rank_img_path)
    plt.imshow(img_r)
    plt.show()
    flag += 1
    # break
