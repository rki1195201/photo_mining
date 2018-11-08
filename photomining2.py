#coding=gbk
import requests
import os
from bs4 import BeautifulSoup
import sys
import warnings
import json

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
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    url = "https://www.google.com/search?q="+name+"&tbm=isch"


    res = requests.get(url,headers=headers)

    soup = BeautifulSoup(res.text,'html.parser')
    #open('soup.txt','wb').write(res.content)
    photo_tag = soup.find_all('img',{'class':'rg_ic'})
    #print(photo_tag)
    k = 0
    createNewFolder(name)

    for tag in photo_tag:
        src = tag.get('data-src')
        #print(src)
        if src!=None:
            r = requests.get(src,allow_redirects=True,verify=False)
            open(name+str(k)+'.jpg','wb').write(r.content)
            k = k + 1
            
    os.chdir(base)