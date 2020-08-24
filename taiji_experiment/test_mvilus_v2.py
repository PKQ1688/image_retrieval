# -*- coding:utf-8 -*-
# @author :adolf
import json
import os
import time

from feature_experiment.test_api import path2base64, getSimilarImages_str, addImages_str
from pathos.multiprocessing import ProcessingPool

img_file_path = "/home/shizai/datadisk5/cv/image_retrieval/taiji_test/"
img_list = os.listdir(img_file_path)

img_id = 3136
img_name = img_list[img_id]

pool = ProcessingPool(100)
file_path = os.path.join(img_file_path, img_name)
fileid = "taiji_test_" + str(img_id)
file_base64 = path2base64(file_path)

s1 = time.time()
# for _ in range(10):
result = pool.map(addImages_str, [fileid] * 100, [file_base64] * 100)
e1 = time.time()
print("get similar use time:", e1 - s1)
print(result)
