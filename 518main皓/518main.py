import requests
from bs4 import BeautifulSoup
import re #正規表示法
import time
import threading
import json
from collections import OrderedDict

global static #增加一個全域變數用來紀錄統計結果
static={}

#打開我們要比對的字典檔--
with open('./wordlen.txt') as f:
    wordlen = f.read().split('\n')
del wordlen[0]
#--

# 一個用來分析內頁的function--
def inner_word(url):
    inner = requests.get(url)  # 用get連到網頁
    innersoup = BeautifulSoup(inner.text, 'lxml')  # 放到BeautifulSoup解析
    innerselect2 = str(innersoup.select_one('div.job-detail-box > dl')).upper()
    # 找到可能會出現找尋目標的區塊將全部英文變大寫
    innerselect = str(innersoup.select_one('div.> p')).upper()
    # 同上
    lan1 = re.findall('[A-Z]+[+#?]*', innerselect)
    # 用正規法抓出每個英文單字
    lan2 = re.findall('[A-Z]+[+#?]*', innerselect2)
    # 同上 第二區塊的
    lan1.extend(lan2)
    # 將兩個list合併
    if 'HTML#' in lan1:
        lan1.remove('HTML#')
    # 排除調內文出現的雜訊
    if 'HTML?' in lan1:
        lan1.remove('HTML?')
    # 雜訊2
    lan1 = list(set(lan1))
    # 清除調list內重複的部份

    for i in lan1:  # 將每個元素都跑過 內容會顯示在i
        if i in wordlen:  # 如果list裡面的字有出現在我們的字典檔中
            if i in static:  # 如果static已經有這個字 就在value+1
                static[i] += 1
            else:
                static[i] = 1  # 如果static統計的字典檔還沒有這個字 就新增
    return static
#--

#這是用來抓出搜尋畫面中所有的case連結--
def page(url):
    res = requests.get(url)
    time.sleep(0.5)
    soup = BeautifulSoup(res.text, 'lxml')
    time.sleep(0.5)
    links = soup.select('li.title > a')
    for link in links:
        inner_word(str(link['href']))#把取得的連結丟到上面inner_word function去解析
        print("%s" %  link['href'])
        print("=" * 50)
    return static
#--

#多線程處理--
class MyClass (threading.Thread):
    def __init__(self,number):
        threading.Thread.__init__(self)
        self.number=number
    def run(self):
        print(('start'+str(self.number)+' '))
        page('https://www.518.com.tw/job-index-P-'+str(self.number)+'.html?i=1&am=1&ab=2032001,2032002,')
        print(('finish'+str(self.number)+' '))
        time.sleep(0.5)
#--

#main--
threads=[]
for i in range(1,54+1):
    Thread=MyClass(i)
    threads.append(Thread)
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

dictlanguage= sorted(static.items(), key=lambda d:d[1],reverse=True) #排序

print(dictlanguage)

language = OrderedDict(dictlanguage)
#輸出成json檔--
with open('../data/518.json', 'w') as f:
    json.dump(language, f)