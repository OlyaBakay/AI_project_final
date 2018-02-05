import torch
import torch.utils.data as data

import os
from PIL import Image
from torchvision import transforms
import pandas as pd
import numpy as np


class ImageDataset(data.Dataset):
    def __init__(self, eq_path, an_path, csv_path, lower_bound=0, upper_bound=1000, transform=None):
        self.eq_path = eq_path
        self.an_path = an_path
        self.csv_path = csv_path
        self.transform = transform
        self.eq_images = []
        self.an_images = []
        self.data_labels = []
        self.answers = []

        eq_filenames = os.listdir(eq_path)
        an_filenames = os.listdir(an_path)

        upper_bound = min(len(eq_filenames), len(an_filenames), upper_bound)

        for eq_filename in eq_filenames[lower_bound:upper_bound]:
            self.eq_images.append(eq_path + "/" + eq_filename)

        for an_filename in an_filenames[lower_bound:upper_bound]:
            self.an_images.append(an_path + "/" + an_filename)

        with open(csv_path) as f:
            df = pd.read_csv(f)
            self.data_labels = df["IsCorrectAnswer"]
            self.answers = df["Answer"]

    def __len__(self):
        return len(self.eq_images)

    def __getitem__(self, index):
        eq_image = Image.open(self.eq_images[index])
        an_image = Image.open(self.an_images[index])

        if self.transform is None:
            self.transform = transforms.Compose([transforms.ToTensor()])

        eq_image = self.transform(eq_image)
        eq_image_sq = eq_image.squeeze()
        an_image = self.transform(an_image)
        an_image_sq = an_image.squeeze()

        image = torch.stack([eq_image_sq, an_image_sq])
        label = self.data_labels[index]
        answer = self.answers[index].astype(np.float32)
        return image, label, eq_image, an_image, answer


if __name__ == "__main__":
    batch_size = 100
    num_of_epochs = 100

    data = "./pics/data"
    labels = "./pics/labels"
    csv_path = "./pics/info.csv"

    train_dataset = ImageDataset(data, labels, csv_path, lower_bound=0, upper_bound=6000)
    test_dataset = ImageDataset(data, labels, csv_path, lower_bound=6000, upper_bound=10000)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

    image, label, eq_image, an_image, answer = train_dataset[0]
