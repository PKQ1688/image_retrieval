# -*- coding:utf-8 -*-
# @author :adolf
import os
import random
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as transforms
from tqdm import tqdm
import cv2
import numpy as np


class TripleDateSet(Dataset):
    def __init__(self, data_path, is_training=True):
        cls_path_list = os.listdir(data_path)
        self.patients = list()

        self.TARGET_IMG_SIZE = 224
        self.transform = transforms.Compose([
            transforms.Resize((self.TARGET_IMG_SIZE, self.TARGET_IMG_SIZE)),
            # transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        for cls_name in tqdm(cls_path_list):
            img_name_path = os.path.join(data_path, cls_name)
            img_name_list = os.listdir(img_name_path)
            for img_name in img_name_list:
                anchor = Image.open(os.path.join(img_name_path, img_name)).convert("RGB")
                # anchor = cv2.imdecode(np.fromfile(os.path.join(img_name_path, img_name), dtype=np.uint8), -1)
                # anchor = Image.fromarray(anchor).convert("RGB")

                pos_name = random.choice(img_name_list)
                positive = Image.open(os.path.join(img_name_path, pos_name)).convert("RGB")
                # positive = cv2.imdecode(np.fromfile(os.path.join(img_name_path, pos_name), dtype=np.uint8), -1)
                # positive = Image.fromarray(positive).convert("RGB")

                neg_cls = random.choice(cls_path_list)
                neg_img_list = os.listdir(os.path.join(data_path, neg_cls))

                neg_img_name = random.choice(neg_img_list)

                negative = Image.open(os.path.join(data_path, neg_cls, neg_img_name)).convert("RGB")
                # print("1111", os.path.join(data_path, neg_cls, neg_img_name))
                # negative = cv2.imdecode(np.fromfile(os.path.join(data_path, neg_cls, neg_img_name), dtype=np.uint8), -1)
                # negative = Image.fromarray(negative).convert("RGB")

                self.patients.append((anchor, positive, negative))

        random.shuffle(self.patients)
        # self.patients = self.patients[:10]

        validation_cases = int(0.1 * len(self.patients))
        # validation_patients = random.sample(self.patients, k=validation_cases)

        if not is_training:
            self.patients = self.patients[-validation_cases:]
        else:
            self.patients = self.patients[:-validation_cases]

        print('data length:', len(self.patients))

    def __len__(self):
        return len(self.patients)

    def __getitem__(self, item):
        anchor, positive, negative = self.patients[item]

        # anchor = anchor.convert("RGB")
        anchor = self.transform(anchor)

        # positive = positive.convert("RGB")
        positive = self.transform(positive)

        # negative = negative.convert("RGB")
        negative = self.transform(negative)

        return anchor, positive, negative
