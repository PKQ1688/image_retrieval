# -*- coding:utf-8 -*-
# @author :adolf
import os
# import json
# from PIL import Image
# import matplotlib.pyplot as plt

from feature_experiment.test_api import *
import time
# import random

from pathos.multiprocessing import ProcessingPool

img_file_path = "/home/shizai/datadisk5/cv/image_retrieval/taiji_test/"
img_list = os.listdir(img_file_path)


def del_some_img(img_nums):
    img_id_list = list(range(img_nums))

    # print(img_id_list)

    for img_id in img_id_list:
        # img_name = img_list[img_id]

        # file_path = os.path.join(img_file_path, img_name)
        fileid = "taiji_test_" + str(img_id)
        # file_base64 = path2base64(file_path)

        # print("file_id")
        # print(fileid)
        result = deleteImages(fileid)

        # print(result)


def add_some_img(img_nums):
    img_id_list = list(range(img_nums))
    for img_id in img_id_list:
        img_name = img_list[img_id]

        file_path = os.path.join(img_file_path, img_name)
        fileid = "taiji_test_" + str(img_id)
        file_base64 = path2base64(file_path)

        result = addImages_str(fileid, file_base64)
        # print(result)


def multi_add_img(img_nums, pool_nums):
    img_id_list = list(range(img_nums))

    file_path_list = [os.path.join(img_file_path, img_list[img_id]) for img_id in img_id_list]
    fileID_list = ["taiji_test_" + str(img_id) for img_id in img_id_list]
    file_base64_list = [path2base64(file_path) for file_path in file_path_list]

    # print(fileID_list)

    pool = ProcessingPool(pool_nums)
    result = pool.map(addImages_str, fileID_list, file_base64_list)

    print(result)


def multi_get_similar_img(img_nums, pool_nums):
    img_id_list = list(range(img_nums))

    s1 = time.time()
    file_path_list = [os.path.join(img_file_path, img_list[img_id]) for img_id in img_id_list]
    fileID_list = ["taiji_test_" + str(img_id) for img_id in img_id_list]
    file_base64_list = [path2base64(file_path) for file_path in file_path_list]
    e1 = time.time()
    print('use time', e1 - s1)

    pool = ProcessingPool(pool_nums)
    result = pool.map(getSimilarImages_str, fileID_list, file_base64_list)

    print(result)


if __name__ == '__main__':
    # s1 = time.time()
    # # add_some_img(1000)
    # del_some_img(1000)
    # e1 = time.time()
    # print('use time', e1 - s1)

    ss = time.time()
    multi_get_similar_img(img_nums=100, pool_nums=10)
    ee = time.time()
    print("multi time:", ee - ss)
