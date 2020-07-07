# -*- coding:utf-8 -*-
# @author :adolf
import requests
import base64

base_url = "http://192.168.1.135:5003/"


def getSimilarImages(file_id_path, file_base64_path):
    url = base_url + "getSimilarImages"
    files = {"FileId": open(file_id_path, 'rb'), "FileImage": open(file_base64_path, 'rb')}
    r = requests.post(url, files=files)
    result_ = r.text
    return result_


def getSimilarImages_str(file_id, file_base64):
    url = base_url + "getSimilarImages"
    data = {"Id": file_id, "Image": file_base64}
    r = requests.post(url, data=data)
    result_ = r.text
    return result_


def addImages(file_id_path, file_base64_path):
    url = base_url + "addImages"
    files = {"FileId": open(file_id_path, 'rb'), "FileImage": open(file_base64_path, 'rb')}
    r = requests.post(url, files=files)
    result_ = r.text
    return result_


def addImages_str(file_id, file_base64):
    url = base_url + "addImages"
    data = {"Id": file_id, "Image": file_base64}
    r = requests.post(url, data=data)
    result_ = r.text
    return result_


def deleteImages(image_id_str):
    url = base_url + "deleteImages"
    # parameters = {"Id": "news1,news2,news3"}
    parameters = {"Id": image_id_str}
    r = requests.post(url, data=parameters)
    result_ = r.text
    return result_


def countImages():
    url = base_url + "countImages"
    r = requests.post(url)
    result_ = r.text
    return result_


def path2base64(img_path):
    with open(img_path, 'rb') as f:
        image = f.read()
        encodestr = str(base64.b64encode(image), 'utf-8')
    return encodestr


if __name__ == '__main__':
    # print(countImages())
    # file_path = '/home/shizai/datadisk5/cv/image_retrieval/taiji_test/9579c1426957e9c4d8b7922e8ab0ffcf.JPEG'
    # fileid = "taiji_test_20"
    # file_base64 = path2base64(file_path)
    # result = getSimilarImages_str(fileid, file_base64)
    # print(result)
    with open("/home/shizai/datadisk2/nlp/taiji/taiji_test_id.txt", "r") as fp:
        line_id = fp.read()
        line_id = line_id.split(',')[:-1]
        # print(line_id)
    with open("/home/shizai/datadisk2/nlp/taiji/taiji_test_base64.txt") as fp:
        line_img = fp.read()
        line_img = line_img.split(',')[:-1]

    for index in range(len(line_id)):
        if index != 26100:
            continue
        print(index)
        file_id = line_id[index]
        file_base64 = line_img[index]
        addImages_str(file_id, file_base64)

# result_count = countImages()
# result_add = addImages("/home/shizai/datadisk2/nlp/taiji/taiji_test_id.txt",
#                        "/home/shizai/datadisk2/nlp/taiji/taiji_test_base64.txt")
# print(result_add)
