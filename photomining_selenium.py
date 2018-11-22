#coding=gbk
from selenium import webdriver
import requests
import os, sys, json, warnings, time
from bs4 import BeautifulSoup

if not sys.warnoptions:
    warnings.simplefilter("ignore")

def createNewFolder(name):
    retval = os.getcwd()
    path = "/"+name
    newpath = retval + path
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)

def createbase():
    retval = os.getcwd()
    path = "/allphoto"
    newpath = retval + path
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)
    return newpath

fp = open('foodlist.json','r')
lines = json.load(fp)
base = createbase()

for line in lines:
    name = line["foodname"]
    print(name)
    my_params = {'q':name,'tbm':'isch'}
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    url = "https://www.google.com/search?q="+name+"&tbm=isch"

    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(0.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    photo_tag = driver.find_elements_by_class_name("rg_ic")

    k = 0
    createNewFolder(name)

    for tag in photo_tag:
        src = tag.get_attribute("src")
        if src!=None and k>20:
            print(src)
            r = requests.get(src,allow_redirects=True,verify=False)
            open(name+str(k)+'.jpg','wb').write(r.content)
        k = k + 1

    driver.quit()
    os.chdir(base)