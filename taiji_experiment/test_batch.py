# -*- coding:utf-8 -*-
# @author :adolf
import cv2
import os
import math
import json
import base64
import argparse
import textwrap
import requests
import numpy as np
from time import time
from os import listdir
from os.path import isfile, join, getsize
import multiprocessing
from PIL import Image, ImageDraw, ImageFont


def add_images(folder_path, ip, port, basenum):
    url = "http://{}:{}/addImages".format(ip, port)
    id = "batch-"
    count = basenum
    for filename in folder_path:
        # print(filename)
        count = count + 1
        print(count)
        with open(filename, 'rb') as f:
            image = f.read()
        encode_stream = str(base64.b64encode(image), 'utf-8')
        payload = {"Id": (id + str(count)), "Image": encode_stream}
        # print((id + str(count)))
        r = requests.post(url, json=payload)
        print("Image: " + (id + str(count)) + " result: " + r.text)
    return 0


def count_images(ip, port):
    url = "http://{}:{}/countImages".format(ip, port)
    p_get = requests.post(url)
    return p_get.text


def get_similar_images(folder_path, ip, port):
    url = "http://{}:{}/getSimilarImages".format(ip, port)
    files = []
    count = 0
    for r, d, f in os.walk(folder_path):
        for file in f:
            filename = os.path.join(r, file)
            files.append(filename)
    for filename in files:
        count = count + 1
        with open(filename, 'rb') as f:
            image = f.read()
        encode_stream = str(base64.b64encode(image), 'utf-8')
        payload = {"Id": "search_test", "Image": encode_stream}
        r = requests.post(url, json=payload)
        print("Image: " + filename + " result: " + r.text)
    return 0


# def delete_images(folder_path, ip, port):
#     url = "http://{}:{}/deleteImages".format(ip, port)
#     id = "test-"
#     for x in range(1, 10000):
#         # print(filename)
#         payload = {"Id": (id + str(x))}
#         r = requests.post(url, json=payload)
#         print("Image: " + (id + str(count)) + " result: " + r.text)
#     return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', '-image_path', type=str, nargs='?', help='image_path')
    parser.add_argument('--ip', '-ip', type=str, default="127.0.0.1",
                        nargs='?', help='ip')
    parser.add_argument('--port', '-port', type=str, default="5000",
                        nargs='?', help='port')
    args = parser.parse_args()
    num_thread = 100
    files = []
    threads = []
    print(args.image_path)
    for r, d, f in os.walk(args.image_path):
        for file in f:
            filename = os.path.join(r, file)
            files.append(filename)

    print(files)
    ts = time()
    # result = add_images(args.image_path, args.ip, args.port)
    for i in range(num_thread):
        divides = math.floor(float(len(files)) / float(num_thread))
        sub_files = files[i * divides:(i + 1) * divides]
        p = multiprocessing.Process(target=add_images, args=(sub_files, args.ip, args.port, i * divides))
        threads.append(p)

    for p in threads:
        p.start()
    for p in threads:
        p.join()
    print(time() - ts)

    print(time() - ts)
    print(count_images(args.ip, args.port))
