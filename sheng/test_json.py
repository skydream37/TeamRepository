#######################import起手式##########################
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import threading
import time

#######################自建字典##########################
wc = Counter()
wc["C"]=0
wc["C++"]=0
wc["C#"]=0
wc["PYTHON"]=0
wc["JAVA"]=0
wc["JAVASCRIPT"]=0
wc["PHP"]=0
wc["HTML"]=0
wc["SQL"]=0
wc["CSS"]=0
wc["R"]=0
wc["CSS"]=0
wc["BASH"]=0
wc["RUBY"]=0
wc["PERL"]=0
wc["SCALA"]=0
wc["SWIFT"]=0
wc["GO"]=0
wc["DELPHI"]=0
wc["TYPESCRIPT"]=0

#######################共用變數##########################
links=[]
host = 'https://www.104.com.tw'

#######################內文爬蟲##########################
def extract(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    tool = []
    target = []
    try:
        for word in soup.select('dd.tool')[0].text.split('、'):  # 每一頁面內的 "擅長工具："欄
            tool.append(word.upper())
        txt = soup.select('div.content')[1].select('dd')[7].text.upper()  # 每一頁面內的 "其他條件："欄
        othercond = re.findall('[A-Z]+[+#-C]*', "%s" % txt)

        for word in othercond:  # 怕有重複值，先用for迴圈檢查
            if word not in target:
                target.append(word)
    except:
        pass

    for abc in tool:  # 找出網頁內的 "擅長工具："欄內的英文單字並與自建字典比較
        if abc in wc:
            wc[abc] += 1
    for abc in target:  # 找出網頁內的 "其他條件："欄內的英文單字並與自建字典比較
        if abc in wc:
            wc[abc] += 1

#######################換頁爬蟲##########################
def pageChange(page):
    host = 'https://www.104.com.tw'  # 改參數i即可換頁（下一行）
    res = requests.get('https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=0&page=' + 'i' + '&psl=N_A')
    txt = soup = BeautifulSoup(res.text, 'lxml')
    address = []
    for href in txt.select('div.jobname_summary > a'):  # 每一頁內各工作的連接網址
        a = href['href']
        print(host+a)
        links.append(host + a)  # 將各內文頁的網址丟入link陣列裡

#######################內文爬蟲執行緒##########################
class textThread (threading.Thread):
    def __init__(self,link): #定義建構子（self為必要(= JAVA裡的this),後面接要輸入的參數）
        threading.Thread.__init__(self)
        self.link=link
    def run(self): #等同於java執行緒中的run 把它overwrite
        extract(self.link)

#######################換頁爬蟲執行緒##########################
class pageThread (threading.Thread): #建立多執行緒類別(內文用)
    def __init__(self,page): #定義建構子（self為必要(= JAVA裡的this),後面接要輸入的參數）
        threading.Thread.__init__(self) #繼承父類別（照著打就好）
        self.page=page #this.page=page
    def run(self): #改寫run方法
        pageChange(self.page) #將要爬的頁數丟給pageChange去執行

#######################執行執行緒##########################
threadpage=[] #（換頁）所有執行緒存放的陣列
for page in range(1,105):
    Thread=pageThread(page)
    threadpage.append(Thread)
for i in threadpage:
    i.start() #執行緒開始
for i in threadpage:
    i.join()  #全部執行緒結束後主執行緒才會繼續（確保所有執行緒都跑完）

threadwords=[] #（爬內文）所有執行緒存放的陣列
for link in links:
    threadword=textThread(link)
    threadwords.append(threadword)
for i in threadwords:
    i.start() #執行緒開始
    time.sleep(0.01)
for i in threadwords:
    i.join() #全部執行緒結束後主執行緒才會繼續（確保所有執行緒都跑完）

#######################印出結果##########################
print('共爬了'+str(len(threadpage))+'頁')
print('共爬了'+str(len(threadwords))+'筆內文')
wc.most_common()

#######################畫圖##########################
import matplotlib.pyplot as plt
import numpy as np

listname = []
listvalue = []
for i in wc.keys():
    listname.append(i)
for v in wc.values():
    listvalue.append(v)

xticks = np.arange(len(listname))
plt.xticks(xticks, list(listname))  # 用作 X 軸刻度的值
plt.xticks(rotation=90)
plt.bar(xticks, listvalue, align='center', color='green')
plt.title("Hot Used Languaage")  # 給標題
plt.show()


import json
data = {
        'c':wc['c'],
        'C++':wc["C++"],
        'C#':wc["C#"],
        'PYTHON':wc["PYTHON"],
        'JAVA':wc["JAVA"],
        'JAVASCRIPT':wc["JAVASCRIPT"],
        'PHP':wc["PHP"],
        'HTML':wc["HTML"],
        'SQL':wc["SQL"],
        'CSS':wc["CSS"],
        'R':wc["R"],
        'BASH':wc["BASH"],
        'RUBY':wc["RUBY"],
        'PERL':wc["PERL"],
        'SCALA':wc["SCALA"],
        'SWIFT':wc["SWIFT"],
        'GO':wc["GO"],
        'DELPHI':wc["DELPHI"],
        'TYPESCRIPT':wc["TYPESCRIPT"],
        }

print(json.dumps(data))
with open('../data/104sheng.json','w') as f:
    json.dump(data,f)