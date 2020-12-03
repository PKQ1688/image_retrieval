# -*- coding:utf-8 -*-
# @author :adolf
# from PIL import Image
import os
# import matplotlib.pyplot as plt
import shutil
import random

img_file = "/home/shizai/data2/ocr_data/tai_use/"

img_file_list = os.listdir(img_file)
# img_name = img_list[13134]
# print(img_name)
# img = Image.open(os.path.join(img_file, img_name))

# for class_img_file in img_file_list:
#     print(class_img_file)
#     class_img_file_list = os.listdir(os.path.join(img_file, class_img_file))
#     for index in range(len(class_img_file_list)):
#         img_name = class_img_file_list[index]
#         print(img_name)
#         os.rename(os.path.join(img_file, class_img_file, img_name),
#                   os.path.join(img_file, class_img_file, class_img_file + "_" + str(index) + ".jpg"))
# break
# plt.imshow(img)
# plt.show()

# with open("/home/shizai/datadisk2/nlp/taiji/taiji_test_id.txt", "r") as fp:
#     line_id = fp.read()
#     line_id = line_id.split(',')[:-1]
#     # print(line_id)
# with open('/home/shizai/datadisk2/nlp/taiji/taiji_test_base64.txt') as fp:
#     line_img = fp.read()
#     line_img = line_img.split(',')[:-1]
# for root, dirs, files in os.walk(img_file):
#     # print(files)
#     for name in files:
#         if "jpg" in name:
#             print(os.path.join(root, name))
#             shutil.move(os.path.join(root, name),
#                         os.path.join("/home/shizai/data2/ocr_data/tai_use", name))
query_list = random.sample(img_file_list, 300)
print(query_list)
for query_name in query_list:
    shutil.copyfile(os.path.join(img_file, query_name),
                    os.path.join("/home/shizai/data2/ocr_data/taiji_query", query_name))
