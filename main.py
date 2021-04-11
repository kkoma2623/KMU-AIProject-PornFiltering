import os
from selenium import webdriver
from tqdm import tqdm
import numpy as np
import PIL.Image as pilimg
from PIL import Image
import matplotlib.pyplot as plt
from urllib import request
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.models as models
import torchvision.utils as utils
import torchvision.datasets as dset
import torchvision.transforms as transforms
import time

class AppURLopener(request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"



def download_imgs(urls):
    url_number = {}
    for i , url in enumerate(urls):
        try:
            savename = str(i) + ".png"
            _urlopener = AppURLopener()
            _urlopener.retrieve(url, os.path.join('img/0',savename))
            url_number[i] = url
            # request.urlretrieve(url, os.path.join('img/0',savename))
        except Exception as e:
            print(url)
            print(e)
            pass
    return url_number



def test(test_data, model, device):
    result = []
    model.to(device)
    ephoc = 0
    index = 0
    for img_i , label_i in test_data:
        img_i , label_i = img_i.view(-1, 3, 224, 224).to(device) , label_i.view(-1)
        outputs = model(img_i)
        _, predicted = torch.max(outputs, 1)
        for i in range(0,len(predicted)):
            if (predicted[i]==0):
                print(img_i[i])
                result.append((ephoc , i))
        ephoc+=1

    return result

if __name__ == "__main__":
    driver = webdriver.Chrome(r'C:\Users\hyeongy\PycharmProjects\AI_detect\chromedriver.exe')
    driver.get('https://ko.chaturbate.com/?tour=LQps&disable_sound=0&join_overlay=1&campaign=pYoNZ&room=akdrh1234')
    #
    urls = []
    url_tag = {}
    imgs_tags = driver.find_elements_by_tag_name("img")
    video_tags = driver.find_elements_by_tag_name("video")
    #
    for i in imgs_tags:
        url = i.get_attribute('src')
        urls.append(url)
        url_tag[url] = i
    print(len(imgs_tags))


    url_number = download_imgs(urls)

    time.sleep(5)

    test_dataset = dset.ImageFolder(root=r"./img",
                                    transform=transforms.Compose([
                                        transforms.Scale(224),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5, 0.5, 0.5),
                                                             (0.5, 0.5, 0.5)),
                                    ]))

    test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=20,
                                                  shuffle=False, )


    print(len(test_dataloader))


    PATH = r'./model/resnet5_224.pth'
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = models.resnet50()
    model.fc = nn.Linear(2048, 2)
    model.load_state_dict(torch.load(PATH))
    model.eval()
    result = test(test_dataloader, model, device)  # test_data , model , device
    print("   ")

    for i in result:
        ephoc = i[0]
        index = i[1]
        url_index = int(str(test_dataset.imgs[(ephoc*20)+index]).split('\\')[4].split(".")[0])
        driver.execute_script("arguments[0].src='http://203.246.112.137/static/a.jpg' ", url_tag[url_number[url_index]])
