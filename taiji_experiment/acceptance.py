# -*- coding:utf-8 -*-
# @author :adolf
import os
import json
from PIL import Image
import matplotlib.pyplot as plt

import time
from feature_experiment.test_api import *
import argparse
from pathos.multiprocessing import ProcessingPool


# img_file_path = "/home/shizai/data2/ocr_data/tai_use"
# img_list = os.listdir(img_file_path)
# img_file_path = "."

def get_acc_result(img_file_path, query_list):
    for img_name in query_list:
        img_path = os.path.join(img_file_path, img_name)
        file_base64 = path2base64(img_path)
        fileid = img_name.split('.')[0]
        result = getSimilarImages_str(fileid, file_base64)
        result = json.loads(result)
        result = result["data"][0]["similarImages"]
        print('1111', result)

        for index, img_dict in enumerate(result):
            print(index)
            # print(img_dict["id"])
            img_x = img_dict["id"].split("_")[-1]
            print(img_x)
            img_path = os.path.join(img_file_path, img_list[int(img_x)])

            # print(img_path)
            img = Image.open(img_path)
            # img.save(os.path.join(result_path, "get_img_" + str(index) + ".jpg"))
            plt.imshow(img)
            plt.title(img_dict["id"])
            plt.show()


def get_test_time(img_file_path, img_list):
    file_id_list = list()
    file_img_list = list()
    size = len(img_list)
    for image_name in img_list:
        fileid = image_name.split('.')[0]
        file_base64 = path2base64(img_path=os.path.join(img_file_path, image_name))
        file_id_list.append(fileid)
        file_img_list.append(file_base64)

    start_time = time.time()
    pool = ProcessingPool(20)
    result = pool.map(getSimilarImages_str, file_id_list, file_img_list)
    end_time = time.time()
    use_time = end_time - start_time
    print("本次共测试{}张图片，总共用时{.2f}秒，平均每张图片用时{.2f}毫秒".format(size, use_time, 1000 * use_time / size))
    return result


def add_all_image(img_file_path, img_list):
    file_id_list = list()
    file_img_list = list()
    for image_name in img_list:
        fileid = image_name.split('.')[0]
        file_base64 = path2base64(img_path=os.path.join(img_file_path, image_name))
        file_id_list.append(fileid)
        file_img_list.append(file_base64)

    file_id_list = file_id_list[9300:]
    file_img_list = file_img_list[9300:]

    assert len(file_id_list) == len(file_img_list)
    # pool = ProcessingPool(10)
    for index in range(len(file_id_list)):
        _ = addImages_str(file_id_list[index], file_img_list[index])
    # result = pool.map(addImages_str, file_id_list, file_img_list)
    # return result


if __name__ == '__main__':
    # add_all_image()
    # print(deleteTable("milvus_image"))
    parser = argparse.ArgumentParser()
    parser.add_argument("--all_image_dir", "-img", type=str, default="/home/shizai/data2/ocr_data/tai_use",
                        nargs="?", help="image_dir")
    parser.add_argument("--query_image_dir", "-q", type=str, default="/home/shizai/data2/ocr_data/taiji_query/",
                        nargs="?", help="query_image_dir")
    parser.add_argument("--scene", "-s", type=str, default="acc",
                        nargs="?", help="scene")
    args = parser.parse_args()

    img_file_path = args.all_image_dir
    query_img_file_path = args.query_image_dir

    img_list = os.listdir(img_file_path)
    query_list = os.listdir(query_img_file_path)

    if args.scene == "add":
        add_all_image(img_file_path, img_list)
    elif args.scene == "acc":
        get_acc_result(query_img_file_path, query_list)
    elif args.scene == "time":
        get_test_time(query_img_file_path, query_list)
