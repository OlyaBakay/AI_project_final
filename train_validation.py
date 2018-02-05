import numpy as np
import torch
import torch.nn as nn
import torch.utils.data as data
from sklearn.metrics import r2_score, f1_score
from torch.autograd import Variable

from datasets import ImageDataset
from models.approximation_net import ApproxNet


def train(use_cuda=False):
    data = "./pics/data"
    labels = "./pics/labels"
    csv_path = "./pics/info.csv"

    batch_size = 100
    num_of_epochs = 20

    train_dataset = ImageDataset(data, labels, csv_path, lower_bound=0, upper_bound=6000)
    test_dataset = ImageDataset(data, labels, csv_path, lower_bound=6000, upper_bound=10000)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

    lr = 0.0002
    criterion = nn.MSELoss()
    model = ApproxNet()

    if use_cuda:
        model = model.cuda()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(num_of_epochs):
        # Training
        for i, (_, _, X, _, y_true) in enumerate(train_loader):
            X = Variable(X)
            y_true = Variable(y_true)
            y_predict = model(X)
            print(y_true.size(), y_predict.size())
            model.zero_grad()
            loss = criterion(y_predict, y_true)
            loss.backward()
            optimizer.step()
            print("Epoch: [{}/{}], Stage: [{}/{}], Loss: {}".format(epoch + 1, num_of_epochs, i + 1, len(train_loader), loss.data[0]))
    #         break
        # Testing
        correct = np.array([])
        predicted = np.array([])
        for (X, y_true) in test_loader:
            X = Variable(X)
            y_out = model(X)
            _, y_pred = torch.max(y_out, 1)
            correct = np.concatenate((correct, y_true.numpy()))
            predicted = np.concatenate((predicted, y_pred.data.numpy()))
        print(correct.shape, predicted.shape)
        print("Epoch: {}, Accuracy: {}%".format(epoch + 1, f1_score(correct, predicted)))