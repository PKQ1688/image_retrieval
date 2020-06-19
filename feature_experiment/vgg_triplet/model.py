# -*- coding:utf-8 -*-
# @author :adolf
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models


class VggTriplet(nn.Module):
    def __init__(self):
        super().__init__()

        self.model = models.vgg16(pretrained=False).features

    def forward(self, anchor, positive, negative):
        an1 = self.model(anchor)
        an1 = F.max_pool2d(an1, kernel_size=an1.size()[-1])

        pos1 = self.model(positive)
        pos1 = F.max_pool2d(pos1, kernel_size=pos1.size()[-1])

        neg1 = self.model(negative)
        neg1 = F.max_pool2d(neg1, kernel_size=pos1.size()[-1])

        return an1, pos1, neg1
