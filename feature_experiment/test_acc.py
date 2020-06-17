# -*- coding:utf-8 -*-
# @author :adolf
from pic_search.src.encoder.encode import img_to_vec
import base64


def path2base64(img_path):
    with open(img_path, 'rb') as f:
        image = f.read()
        encodestr = str(base64.b64encode(image), 'utf-8')
    return encodestr


img_path_1 = "test_pic/1.png"
img_path_2 = "test_pic/2.png"
img_path_3 = "test_pic/3.png"

img_list = list()
img_list.append(path2base64(img_path_1))
img_list.append(path2base64(img_path_2))
img_list.append(path2base64(img_path_3))

norm_feat_list = img_to_vec(img_list)
