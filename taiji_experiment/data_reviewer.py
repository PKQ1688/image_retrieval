# -*- coding:utf-8 -*-
# @author :adolf
from PIL import Image
import os
import matplotlib.pyplot as plt

img_file = "/home/shizai/datadisk5/cv/image_retrieval/taiji_test"

img_list = os.listdir(img_file)
img_name = img_list[26101]
print(img_name)
img = Image.open(os.path.join(img_file, img_name))

plt.imshow(img)
plt.show()

# with open("/home/shizai/datadisk2/nlp/taiji/taiji_test_id.txt", "r") as fp:
#     line_id = fp.read()
#     line_id = line_id.split(',')[:-1]
#     # print(line_id)
# with open('/home/shizai/datadisk2/nlp/taiji/taiji_test_base64.txt') as fp:
#     line_img = fp.read()
#     line_img = line_img.split(',')[:-1]

