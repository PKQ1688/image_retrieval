# -*- coding:utf-8 -*-
# @author :adolf
import torch
import torchvision.models as models
import torch.nn.functional as F
import torchvision.transforms as transforms

import base64
from PIL import Image
from io import BytesIO

from numpy import linalg as LA


class Img2Vec(object):
    def __init__(self, model_path=None):
        self.TARGET_IMG_SIZE = 224
        self.transform = transforms.Compose([
            transforms.Resize((self.TARGET_IMG_SIZE, self.TARGET_IMG_SIZE)),
            # transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.vgg16(pretrained=True).features
        if model_path is not None:
            model_dict = self.model.state_dict()
            pre_model = torch.load(model_path)
            for k, v in pre_model.items():
                # print('pre_state_dict', k)
                model_dict[k.replace('vgg.', '')] = v

            # pre_state_dict = {k: v for k, v in pre_model.items() if k in model_dict.keys()}
            # print('pre_state_dict')
            # print('model_dict_111', model_dict.keys())
            # model_dict.update(pre_state_dict)
            # print('model_dict_222', model_dict.keys())

            self.model.load_state_dict(model_dict)
        self.model.to(self.device)
        self.model.eval()

    @staticmethod
    def base64_pil(base64_str):
        image = base64.b64decode(base64_str)
        image = BytesIO(image)
        image = Image.open(image)
        return image

    def feature_extraction(self, img_tensor):
        img_tensor = img_tensor.to(self.device)

        with torch.no_grad():
            feature_map = self.model(img_tensor)

            feature_vector = F.max_pool2d(feature_map, kernel_size=feature_map.size()[-1])

        # print('1111', feature_vector.shape)
        feature_vector = torch.squeeze(feature_vector, 3)
        feature_vector = torch.squeeze(feature_vector, 2)
        feature_vector = feature_vector.data.cpu().numpy()

        return feature_vector

    def __call__(self, base64list):
        img_list = [self.base64_pil(base64img) for base64img in base64list]

        img_list = [img.convert("RGB") for img in img_list]
        img_list = [self.transform(img) for img in img_list]

        img_tensor = torch.stack(img_list, dim=0)

        feature_vector = self.feature_extraction(img_tensor)

        # print(feature_vector.shape)

        return feature_vector

        # norm_feat_list = list()

        # for i in range(feature_vector.shape[0]):
        #     norm_feat = feature_vector[i] / LA.norm(feature_vector[i])
        #     norm_feat = [i.item() for i in norm_feat]
        #     norm_feat_list.append(norm_feat)

        # return norm_feat_list


if __name__ == '__main__':
    import os
    import time

    os.environ["CUDA_VISIBLE_DEVICES"] = "1"


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
    # img_list.append(path2base64(img_path_2))
    # img_list.append(path2base64(img_path_3))

    img_to_vec = Img2Vec()

    s1 = time.time()
    norm_feat_list = img_to_vec(img_list)
    print(norm_feat_list)
    s2 = time.time()
    print('use time:', s2 - s1)
