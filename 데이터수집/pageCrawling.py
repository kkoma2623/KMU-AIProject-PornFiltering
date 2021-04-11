import requests
from bs4 import BeautifulSoup
import urllib.request
import hashlib
import os
import shutil

#md5
def getHash(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
#이미지 저장 시도
def tryUrl(dirPath,img_url):
    origin_path = dirPath
    print(img_url)
    path = dirPath + str('a') + '.png'
    urllib.request.urlretrieve(img_url, path)
    new_path = os.path.join(origin_path, getHash(path) + '.gif')
    shutil.move(path, new_path)
#main
def imageDownload(pageUrl,dirPath):
    dirPath= dirPath+r"\\"
    req = requests.get(pageUrl)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_urls = soup.select('img')
    for url in my_urls:
        img_src = url.get('src')
        img_url = str(img_src)
        if img_url.find('http') == 0 or img_url.find('https') == 0:
            try:
                tryUrl(dirPath,img_url)
            except:
                continue
        else:
            back = pageUrl.split('/')[:-1]
            page_url = ''
            for i in back:
                page_url += i + '/'
            page_url = page_url + img_url
            try:
                tryUrl(dirPath, page_url)
            except:
                continue
#테스트 실행
#with open('cr1.json',encoding='utf-8') as data_file:
#    data = json.load(data_file)
#for pageUrl in data:
imageDownload('https://www.bestpornbabes.com/',r"C:\Users\Dalpha\PycharmProjects\untitled\img2")
#print(set(success_list))