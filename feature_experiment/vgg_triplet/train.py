# -*- coding:utf-8 -*-
# @author :adolf
from feature_experiment.vgg_triplet.model import VggTriplet
from feature_experiment.vgg_triplet.dataset import TripleDateSet
from feature_experiment.vgg_triplet import lr_scheduler

import os
import numpy as np
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torch.nn.functional as F


class TrainTool(object):
    def __init__(self,
                 data_path,
                 batch_size=16,
                 workers=0,
                 epochs=5,
                 lr=1e-5):
        self.data_path = data_path
        self.model_path = 'model/vgg_triplet_v2.pth'

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.batch_size = batch_size
        self.workers = workers
        self.epochs = epochs
        self.lr = lr

        self.train_datasets, self.valid_datasets = self.init_datasets()
        self.train_loader, self.valid_loader = self.data_loaders()

        self.model = VggTriplet()
        # self.model.apply(self.weights_init)

        self.model = self.model.to(self.device)

        self.criterion = nn.TripletMarginLoss(margin=1.0, p=2)
        self.optimizer = optim.Adam(self.model.parameters())

        self.val_best_acc = 0

        self.scheduler = lr_scheduler.LR_Scheduler_Head(mode='poly',
                                                        base_lr=self.lr,
                                                        num_epochs=self.epochs,
                                                        iters_per_epoch=len(self.train_loader),
                                                        warmup_epochs=1)

    @staticmethod
    def weights_init(m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            m.weight.data.normal_(0.0, 0.02)
        elif classname.find('BatchNorm') != -1:
            m.weight.data.normal_(1.0, 0.02)
            m.bias.data.fill_(0)

    def init_datasets(self):
        train_datasets = TripleDateSet(data_path=self.data_path,
                                       is_training=True)
        # valid_datasets = train_datasets
        valid_datasets = TripleDateSet(data_path=self.data_path,
                                       is_training=False)

        return train_datasets, valid_datasets

    def data_loaders(self):
        loader_train = data.DataLoader(
            self.train_datasets,
            batch_size=self.batch_size,
            shuffle=True,
            drop_last=False,
            num_workers=self.workers,
            pin_memory=False
        )

        loader_valid = data.DataLoader(
            self.valid_datasets,
            batch_size=1,
            drop_last=False,
            num_workers=self.workers,
        )

        return loader_train, loader_valid

    def train_one_epoch(self, epoch):
        self.model.train()
        for batch_idx, (anchor, positive, negative) in enumerate(self.train_loader):

            self.scheduler(self.optimizer, batch_idx, epoch, self.val_best_acc)

            anchor = anchor.to(self.device)
            positive = positive.to(self.device)
            negative = negative.to(self.device)

            an1, pos1, neg1 = self.model(anchor, positive, negative)

            loss = self.criterion(an1, pos1, neg1)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            if batch_idx % 50 == 0:
                print('Epoch:[{}/{}]\t iter:[{}]\t loss={:.5f}\t lr={}'
                      .format(epoch, self.epochs, batch_idx, loss, self.optimizer.param_groups[0]['lr']))

    def val_model(self):
        self.model.eval()
        total = self.valid_loader.dataset.__len__()
        correct = 0
        for anchor, positive, negative in self.valid_loader:
            anchor = anchor.to(self.device)
            positive = positive.to(self.device)
            negative = negative.to(self.device)

            an1, pos1, neg1 = self.model(anchor, positive, negative)

            an1_vector = torch.squeeze(an1)
            an1_vector = an1_vector.data.cpu().numpy()

            pos1_vector = torch.squeeze(pos1)
            pos1_vector = pos1_vector.data.cpu().numpy()

            neg1_vector = torch.squeeze(neg1)
            neg1_vector = neg1_vector.data.cpu().numpy()

            # print('an1_vector', an1_vector)
            # print('pos1_vector', pos1_vector)
            # print('neg1_vector', neg1_vector)

            dist1 = np.linalg.norm(an1_vector - pos1_vector)
            dist2 = np.linalg.norm(an1_vector - neg1_vector)

            # print('dist1', dist1)
            # print('dist2', dist2)

            if dist1 < dist2:
                correct += 1
        # print('correct', correct)
        # print('total', total)
        acc = correct / total * 1.0

        return acc

    def main(self):
        for epoch in tqdm(range(self.epochs), total=self.epochs):
            self.train_one_epoch(epoch)
            val_acc = self.val_model()
            print('verification accuracy:', val_acc)
            if val_acc > self.val_best_acc:
                torch.save(self.model.state_dict(), self.model_path)


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "2"

    trainer = TrainTool(data_path="baidu_pic/baidu_pic")

    trainer.main()
