import requests as r
from bs4 import BeautifulSoup
import re
from collections import Counter
import threading
import time


def getLink(page): #把搜尋頁丟近來抓連結的function
    print('thread'+str(page)+'start') #測試多執行緒有沒有在動
    time.sleep(2)
    res = r.get("https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=104_bank1&ro=0&area=6001001000%2C6001002000&indcat=1001001000&order=2&asc=0&page={}".format(page)+"&psl=N_A")
    time.sleep(0.1)
    soup = BeautifulSoup(res.text,'lxml')
    time.sleep(0.1)
    links = ['https://www.104.com.tw' + link['href'] for link in soup.select('div.jobname_summary.job_name > a')]
    time.sleep(0.1)
    print(len(links))
    time.sleep(0.1)
    global alinks #拿到外面alinks的值如果沒有加global會變成自己增加區域變數
    alinks += links #alinks = alinks + links

#     print('thread '+str(page)+' end ')


class getLinkThread (threading.Thread): #多線程處理
    def __init__(self,page): #建構子（可以用來傳遞參數）（ex.我要傳入number這個參數讓每一條執行序可以跑不同頁
        threading.Thread.__init__(self) #繼承父類別（照著打就好）
        self.page=page #this.page=page
    def run(self): #等同於java執行緒中的run 把它overwrite
        getLink(self.page) #將要爬的頁數丟給getLink去執行


def getWord(link): #把網址丟進來提取文字後做統計的function
    print(link)
    time.sleep(0.1)
    res = r.get(link)
    time.sleep(0.1)
    soup = BeautifulSoup(res.text,'lxml')
    time.sleep(0.1)
    list1 = str(soup.select('dd.tool > a')).upper() #擅長工具
    time.sleep(0.1)
    list2 = str(soup.select('div.content')).upper() #內文
    time.sleep(0.1)
    list3 = list1 + list2
    time.sleep(0.1)
    words = list(set(re.findall('[A-Z]+[+#]*' , list3)))#擅長工具＋內文 中的所有英文單字
    time.sleep(0.1)
#     time.sleep(0.2)

    for word in words: # 計算所有英文單字的數量
        time.sleep(0.1)
        global wc
        if word in wc:
            wc[word] += 1
        else:
            wc[word] = 1


class getWordThread (threading.Thread): #多線程處理
    def __init__(self,link): #建構子（可以用來傳遞參數）（ex.我要傳入number這個參數讓每一條執行序可以跑不同頁
        threading.Thread.__init__(self)
        self.link=link
    def run(self): #等同於java執行緒中的run 把它overwrite
        getWord(self.link)


# 第一頁開始：
url = 'https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=104_bank1&ro=0&jobcat=2007000000&order=2&asc=0&page=1'
res = r.get(url)
soup = BeautifulSoup(res.text, 'lxml')
links = soup.select('div.jobname_summary.job_name > a')  # 裡面是沒有HOST的
HOST = 'https://www.104.com.tw'
link_list = [HOST + link['href'] for link in links]  # 把裡面每一個網址都加上HOST
# 把link全加到link_list裡面


# 換頁：
buttons = soup.select('span > a')
first_page = 1
# int(buttons[3]['onclick'].split('gopage(')[1].split(');return')[0]) - 2 #3-2
# 顯示當前頁面＋當頁所以職缺(一次爬?頁)
# 把當頁所有職缺的網址放到alink裡面
alinks = []
page_to_crawl = 10  # 要爬幾頁
threads = []
for page in range(1, 151):
    Thread = getLinkThread(page)
    threads.append(Thread)
for i in threads:
    i.start()  # 執行緒開始
# time.sleep(1)
for i in threads:
    i.join()

# print("current page {}".format("https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=104_bank1&ro=0&area=6001001000%2C6001002000&indcat=1001001000&order=2&asc=0&page=".format(page)+"&psl=N_A"))
#     res = r.get("https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=104_bank1&ro=0&area=6001001000%2C6001002000&indcat=1001001000&order=2&asc=0&page={}".format(page)+"&psl=N_A")
#     soup = BeautifulSoup(res.text,'lxml')
#     links = ['https://www.104.com.tw' + link['href'] for link in soup.select('div.jobname_summary.job_name > a')]
#     print(len(links))
#     alinks += links #alinks = alinks + links
#     time.sleep(0.5)


# for i in range(1,10+1):
#     Thread=MyClass(i)
#     threads.append(Thread)
# for thread in threads:
#     thread.start() #執行緒開始
# for thread in threads:
#     thread.join()#等同於java中的join 所有執行序跑完在繼續執行下一行指令
#     getLink(page)



# 小整合：
wc = Counter()  # word count   wc是k:v的形式-> ‘MYSQL': 4’
result_dict = {}
threadwords = []
for link in alinks:
    threadword = getWordThread(link)
    threadwords.append(threadword)
for i in threadwords:
    i.start()  # 執行緒開始
    time.sleep(0.01)
# time.sleep(0.5)
for i in threadwords:
    i.join()

# res = r.get(link)
#         soup = BeautifulSoup(res.text,'lxml')
#         list1 = str(soup.select('dd.tool > a')).upper() #擅長工具
#         list2 = str(soup.select('div.content')).upper() #內文
#         list3 = list1 + list2
#         words = list(set(re.findall('[A-Z]+[+#]*' , list3)))#擅長工具＋內文 中的所有英文單字

#         for word in words: # 計算所有英文單字的數量
#             if word in wc:
#                 wc[word] += 1
#             else:
#                 wc[word] = 1


#     continue
#     print(link) #有一些廣告或外包網continue

string = 'C|C++|C#|PYTHON|JAVA|JAVASCRIPT|PHP|HTML|SQL|CSS|R|BASH|RUBY|PERL|SCALA|SWIFT|GO|DELPHI|TYPESCRIPT|MYSQL'
langs = string.split('|')  # string裡面的語言切開

for lang in langs:  # 每一個語言
    if lang in wc.keys():  # 如果有在wc的key裡的話
        result_dict[lang] = wc[lang]  # lang是key ;wc[lang]語言數量是value

result_dict