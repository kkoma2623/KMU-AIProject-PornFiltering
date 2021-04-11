'''
개인정보 문제로 로그인 부분을 제거하였습니다.
'''

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
f = open("face.txt", 'a')
num = 0

url = "https://www.instagram.com/explore/tags/selfie/"
DRIVER_DIR = r"C:\webdriver\chromedriver.exe"
driver = webdriver.Chrome(DRIVER_DIR)
driver.implicitly_wait(5)
driver.get(url)
totalCount = driver.find_element_by_class_name('FFVAD').text
elem = driver.find_element_by_tag_name("body")
alt_list = []

pagedowns = 1
while pagedowns < 50:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        img = driver.find_elements_by_css_selector('div.KL4Bh > img')
        for i in img:
            img_alt = i.get_attribute('alt')
            alt_list = img_alt.split()
            if '사람' in alt_list and '근접' in alt_list:
                img_src = str(i.get_attribute('src'))
                print(img_src)
                f.write(img_src + '\n')
                urllib.request.urlretrieve(img_src, './face/' + str(num) + '.png')
                num+=1
            else:
                continue
        pagedowns += 1
alt_list = list(set(alt_list))


driver.close()