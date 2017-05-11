import requests
from bs4 import BeautifulSoup
import re
import json
from collections import Counter
import threading
import time

wc = Counter()
wc["C"] = 0
wc["C++"] = 0
wc["C#"] = 0
wc["PYTHON"] = 0
wc["JAVA"] = 0
wc["JAVASCRIPT"] = 0
wc["PHP"] = 0
wc["HTML"] = 0
wc["SQL"] = 0
wc["CSS"] = 0
wc["R"] = 0
wc["BASH"] = 0
wc["RUBY"] = 0
wc["PERL"] = 0
wc["SCALA"] = 0
wc["SWIFT"] = 0
wc["GO"] = 0
wc["DELPHI"] = 0
wc["TYPESCRIPT"] = 0

url = 'https://www.ptt.cc/bbs/Soft_Job/index1247.html'
# ptt最新頁面

HOST = 'https://www.ptt.cc'
headers = {"cookie":"over18=1;"}

# 爬內文
def ptt(each_link):
    res = requests.get(each_link, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    content = soup.select_one('#main-content')  # 內文
    for trash in soup.select('div.article-metaline') + soup.select('div.article-metaline-right') + soup.select(
            'div.push') + soup.select('a') + soup.select('span') + soup.select('script'):
        trash.decompose()
    words = list(set(re.findall('[A-Z]+[+#]*', content.text, re.IGNORECASE)))  # 不處理大小寫,set處理重複問題
    for language in words:
        if language.upper() in wc.keys():
            wc[language.upper()] += 1

def getLink(page) :
    if page % 1 == 0:
        print('[Debug] current page is {}'.format(page))
    try:
        res = requests.get(HOST + "/bbs/Soft_Job/index{}.html".format(page), headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        links = soup.select('div.title > a')
        for link in links:  # link 是每一篇文
            if '徵才' in link.text:
                #                 print(link.text)
                each_link = HOST + link['href']
                #                 print(each_link)
                ptt(each_link)
    except Exception as e:
        print(e, link['href'])

class getLinkThread(threading.Thread):  # 多線程處理
    def __init__(self, page):  # 建構子（可以用來傳遞參數）（ex.我要傳入number這個參數讓每一條執行序可以跑不同頁
        threading.Thread.__init__(self)  # 繼承父類別（照著打就好）
        self.page = page  # this.page=page
    def run(self):  # 等同於java執行緒中的run 把它overwrite
        getLink(self.page)  # 將要爬的頁數丟給getLink去執行

#換頁
res = requests.get(url,headers = headers)
soup = BeautifulSoup(res.text,'lxml')
buttons = soup.select('a.btn.wide')
total_page = int(buttons[1]['href'].split('index')[1].split('.html')[0])+1
page_to_crawl = 1248

threads=[]
for page in range(total_page, total_page - page_to_crawl, -1): #單頁
    Thread = getLinkThread(page)
    threads.append(Thread)
for i in threads:
    i.start()  #執行緒開始
for i in threads:
    i.join()

print(wc)

data={
    'C': wc['C'],
    'C++':wc['C++'],
    'C#': wc['C#'],
    'PYTHON': wc['PYTHON'],
    'JAVA': wc['JAVA'],
    'JAVASCRIPT': wc['JAVASCRIPT'],
    'PHP': wc['PHP'],
    'HTML': wc['HTML'],
    'SQL': wc['SQL'],
    'CSS': wc['CSS'],
    'R': wc['R'],
    'BASH': wc['BASH'],
    'RUBY': wc['RUBY'],
    'PERL': wc['PERL'],
    'SCALA': wc['SCALA'],
    'SWIFT': wc['SWIFT'],
    'GO': wc['GO'],
    'DELPHI': wc['DELPHI'],
    'TYPESCRIPT': wc['TYPESCRIPT']
}

print(json.dumps(data))
with open('../data/ptt_threading.json','w') as f:
    json.dump(data,f)


