# -*- coding:utf-8 -*-
# @author :adolf
import json
import torch
from PIL import Image
import torch.nn as nn
from numpy import linalg as LA
from torchvision import transforms
from efficientnet_pytorch import EfficientNet

model_name = 'efficientnet-b0'
image_size = EfficientNet.get_image_size(model_name)  # 224

model = EfficientNet.from_pretrained(model_name)

tfms = transforms.Compose([transforms.Resize((image_size, image_size)),
                           transforms.ToTensor(),
                           transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])


def extract_feature_efficientnet(img_path):
    img = Image.open(img_path).convert('RGB')
    img = tfms(img).unsqueeze(0)
    features = model.extract_features(img)
    print(features.shape)
    max_pool = nn.MaxPool2d(7, stride=1)
    features = max_pool(features)
    result = torch.squeeze(features)
    result = result.data.cpu().numpy()

    norm_feat = result / LA.norm(result)
    norm_feat = [i.item() for i in norm_feat]

    return norm_feat


img_path = '/data/shiyu/test/1.png'
res_feat = extract_feature_efficientnet(img_path)
print(len(res_feat))
print(res_feat)
