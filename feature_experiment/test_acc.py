# -*- coding:utf-8 -*-
# @author :adolf
import os

from pic_search.src.encoder.encode import Img2Vec
from PIL import Image


class MetricResult(object):
    def __init__(self):
        self.feature_vec = Img2Vec()
        self.transform = self.feature_vec.transform

    def get_vec(self, img_path):
        img = Image.open(img_path).convert("RGB")
        img_tensor = self.transform(img)

        feature = self.feature_vec.feature_extraction(img_tensor)

        return feature


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"

    print(MetricResult().get_vec("test_pic/1.png"))


