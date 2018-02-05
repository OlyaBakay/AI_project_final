import torch.nn.functional as F
import torch.nn as nn


class ValidationNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_1 = nn.Conv2d(2, 32, 3, padding=2)
        self.conv_1_pool = nn.MaxPool2d(2)
        self.conv_2 = nn.Conv2d(32, 64, 3, padding=2)
        self.conv_2_pool = nn.MaxPool2d(2)
        self.conv_2_drop = nn.Dropout2d(0.25)
        self.conv_3 = nn.Conv2d(64, 128, 3, padding=2)
        self.conv_3_pool = nn.MaxPool2d(2)
        self.conv_4 = nn.Conv2d(128, 256, 3, padding=2)
        self.conv_4_pool = nn.MaxPool2d(2)
        self.conv_4_drop = nn.Dropout2d(0.25)
        self.fc_1 = nn.Linear(9216, 84)
        self.fc_2 = nn.Linear(84, 2)

    def forward(self, x):
        x = self.conv_1_pool(F.relu(self.conv_1(x)))
        x = self.conv_2_drop(self.conv_2_pool(F.relu(self.conv_2(x))))
        x = self.conv_3_pool(F.relu(self.conv_3(x)))
        x = self.conv_4_drop(self.conv_4_pool(F.relu(self.conv_4(x))))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc_1(x))
        x = self.fc_2(x)
        return x
