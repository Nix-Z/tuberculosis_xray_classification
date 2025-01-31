import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
import requests
from PIL import Image
from io import BytesIO
import torch
from torchvision.datasets import ImageFolder
from torchvision import datasets
import pickle
from datavisualization import visualize_data

def transform_data():
    path, normal_images, tuberculosis_images = visualize_data()
    
    data_transform = torchvision.transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    total_list = normal_images + tuberculosis_images
    model_dataset = datasets.ImageFolder(path, transform=data_transform)
    img, ann = model_dataset[0]
    print("iiiiiiii",img)
    print("aaaaaaaaa:",ann)
    with open('model_dataset.pkl', 'wb') as f:
        pickle.dump(model_dataset, f)
    return model_dataset

transform_data()
