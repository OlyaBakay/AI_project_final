import torch.nn.functional as F
import torch.nn as nn


class ApproxNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_1 = nn.Conv2d(1, 32, 3)
        self.conv_1_pool = nn.MaxPool2d(2)
        self.conv_2 = nn.Conv2d(32, 64, 3)
        self.conv_2_pool = nn.MaxPool2d(2)
        self.conv_2_drop = nn.Dropout2d(0.25)
        self.conv_3 = nn.Conv2d(64, 128, 3)
        self.conv_3_pool = nn.MaxPool2d(2)
        # self.conv_4 = nn.Conv2d(128, 256, 3)
        # self.conv_4_pool = nn.MaxPool2d(2)
        # self.conv_4_drop = nn.Dropout2d(0.25)
        self.fc_1 = nn.Linear(2304, 512)
        self.fc_1_drop = nn.Dropout2d(0.25)
        self.fc_2 = nn.Linear(512, 64)
        self.fc_2_drop = nn.Dropout2d(0.25)
        self.fc_3 = nn.Linear(64, 8)
        self.fc_4 = nn.Linear(8, 1)

    def forward(self, x):
        x = self.conv_1_pool(F.relu(self.conv_1(x)))
        x = self.conv_2_pool(F.relu(self.conv_2(x)))
        x = self.conv_3_pool(F.relu(self.conv_3(x)))
        # x = self.conv_4_drop(self.conv_4_pool(F.relu(self.conv_4(x))))
        x = x.view(x.size(0), -1)

        x = self.fc_1_drop(F.relu(self.fc_1(x)))
        x = self.fc_2_drop(F.relu(self.fc_2(x)))
        x = F.relu(self.fc_3(x))
        x = self.fc_4(x)

        return x
