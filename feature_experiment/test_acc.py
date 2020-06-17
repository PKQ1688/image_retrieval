# -*- coding:utf-8 -*-
# @author :adolf
import os
import random
import numpy as np

# from pic_search.src.encoder.encode import Img2Vec
from pic_search.src.encoder.encode_efficientent import Img2Vec
from PIL import Image


class MetricResult(object):
    def __init__(self):
        # model_name="efficientnet-b1"
        self.feature_vec = Img2Vec(model_name="efficientnet-b7")
        self.transform = self.feature_vec.transform

    def get_vec(self, img):
        img = img.convert("RGB")
        # img = Image.open(img_path).convert("RGB")
        img_tensor = self.transform(img)
        img_tensor = img_tensor.unsqueeze(0)
        feature = self.feature_vec.feature_extraction(img_tensor)

        return feature

    def get_smi(self, img1, img2):
        # img1 = Image.open(path1)
        # img2 = Image.open(path2)

        vec1 = self.get_vec(img1)
        vec2 = self.get_vec(img2)

        dist = np.linalg.norm(vec1 - vec2)
        return dist

    def calculation_accuracy(self, ori_img, pos_img, neg_img):

        pos_dist = self.get_smi(ori_img, pos_img)
        neg_dist = self.get_smi(ori_img, neg_img)

        if neg_dist > pos_dist:
            return True
        else:
            return False

    def get_acc(self, pos_cls_path, neg_cls_path):
        pos_img_list = os.listdir(pos_cls_path)
        neg_img_list = os.listdir(neg_cls_path)

        pos_imgs = random.sample(pos_img_list, 2)
        neg_imgs = random.choice(neg_img_list)

        ori_path = os.path.join(pos_cls_path, pos_imgs[0])
        pos_path = os.path.join(pos_cls_path, pos_imgs[1])
        neg_path = os.path.join(neg_cls_path, neg_imgs)

        ori_img = Image.open(ori_path)
        pos_img = Image.open(pos_path)
        neg_img = Image.open(neg_path)

        return self.calculation_accuracy(ori_img, pos_img, neg_img)

    def acc_metric(self, test_length=500):
        img_root_path = 'baidu_pic/baidu_pic/'
        cls_path_list = os.listdir(img_root_path)
        # print(cls_path_list)
        correct_result = 0
        for i in range(test_length):
            calculation_list = random.sample(cls_path_list, 2)
            pos_cls_path = os.path.join(img_root_path, calculation_list[0])
            neg_cls_path = os.path.join(img_root_path, calculation_list[1])
            # print('pos_cls_name', calculation_list[0])
            # print('neg_cls_name', calculation_list[1])
            try:
                if self.get_acc(pos_cls_path, neg_cls_path):
                    correct_result += 1
            except Exception as e:
                print(e)
                correct_result += 1

        acc = correct_result / test_length * 1.0
        print(acc)
        return acc


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"

    # path1 = "test_pic/1.png"
    # path2 = "test_pic/2.png"
    # img1 = Image.open(path1)
    # img2 = Image.open(path2)
    metric = MetricResult()
    acc_sum = 0
    for i in range(3):
        acc = metric.acc_metric()
        acc_sum += acc
    print('mean acc', acc_sum / 3)
