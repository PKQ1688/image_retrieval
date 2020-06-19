# -*- coding:utf-8 -*-
# @author :adolf
import os
import base64


def path2base64(img_path):
    with open(img_path, 'rb') as f:
        image = f.read()
        encodestr = str(base64.b64encode(image), 'utf-8')
    return encodestr


def one_file_path(file_path):
    # print(file_path)
    file_name = file_path.split('/')[-1]
    print(file_name)
    img_list = os.listdir(file_path)
    with open('baidu_pic/base64_pic/' + file_name + '_id.txt', 'w') as fp:
        for i in range(len(img_list)):
            fp.write(file_name + '_' + str(i))
            fp.write(',')

    with open('baidu_pic/base64_pic/' + file_name + '_base64.txt', 'w') as fp:
        for img_name in img_list:
            img_path = os.path.join(file_path, img_name)
            # print(img_path)
            base64_encoder = path2base64(img_path)
            fp.write(base64_encoder)
            fp.write(',')


if __name__ == '__main__':
    # file_path = "baidu_pic/baidu_pic/5G"
    # one_file_path(file_path)
    data_path = "baidu_pic/baidu_pic/"
    cls_list = os.listdir(data_path)
    for cls_name in cls_list:
        file_path = os.path.join(data_path, cls_name)
        one_file_path(file_path)
