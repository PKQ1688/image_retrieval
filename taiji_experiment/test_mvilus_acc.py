# -*- coding:utf-8 -*-
# @author :adolf
import os
import json
from PIL import Image
import matplotlib.pyplot as plt

import time
from feature_experiment.test_api import *

img_file_path = "/home/shizai/datadisk5/cv/image_retrieval/taiji_test/"
img_list = os.listdir(img_file_path)

img_id = 3452
img_name = img_list[img_id]
# print(img_name)
file_path = os.path.join(img_file_path, img_name)
fileid = "taiji_test_" + str(img_id)
file_base64 = path2base64(file_path)

s1 = time.time()
for _ in range(10):
    result = getSimilarImages_str(fileid, file_base64)
e1 = time.time()

print("get similar use time:",e1 - s1)
result = json.loads(result)
result = result["data"][0]["similarImages"]
print('1111', result)

# print(file_path)
img_q = Image.open(file_path)
plt.imshow(img_q)
plt.show()

for img_dict in result:
    # print(img_dict["id"])
    img_x = img_dict["id"].split("_")[-1]
    print(img_x)
    img_path = os.path.join(img_file_path, img_list[int(img_x)])
    # print(img_path)
    img = Image.open(img_path)
    plt.imshow(img)
    plt.title(img_dict["id"])
    plt.show()
