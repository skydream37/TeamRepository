#====起手式
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter      # counter (dict形式）
import threading
import time
import csv
global all_case
all_case=0

#########  每個標題頁 def
host = 'https://www.518.com.tw'
links_al = []

def getlink(i):
    res = requests.get(host+'/job-index-P-'+str(i)+'.html?i=1&am=1&ab=2032001')    # '下一頁'組合
    soup = BeautifulSoup(res.text,'lxml')
    links = soup.select('li.title > a')                  # 每一頁的 '標題頁'連結
    for link in links :                                  # '標題頁'連結 取出
        l = link['href']
        links_al.append(l)



#########  每個標題頁thread
class getlinkThread(threading.Thread):
    def __init__(self,link):
        threading.Thread.__init__(self)
        self.link = link
    def run(self):               # run getlink 的方法 裡面的 link['href']
        getlink(self.link)


######### 內文 def
def getinner(inner):
    res = requests.get(inner)
    soup = BeautifulSoup(res.text, 'lxml')
    global all_case
    all_case=all_case+1
    try:
        line1 = soup.select_one('div.JobDescription > p').text   # 工作內容
        line2 = soup.select_one('div.job-detail-box > dl').text  # 擅長工具
        line3 = line1 + line2                          # list 合併
        up = line3.upper()                             # 統一轉為大寫處理
        line = re.findall('[A-Z]+[+#-C]*', "%s" % up)  # 找正規化後的字串

        line_c = []                       # 給他有一個排序的位置放
        for line_check in line:           # 將'正規化'好的 line 放入自定義的 line_check
            if line_check not in line_c:  # 將不再line_check 的英文單字放入line_c(為了不讓值重複)
                line_c.append(line_check)

        for language in line_c:         # 把整理好的line_c 值取出到自定義的 language (list形式)
            global wc                   # 全域變數
            if language in wc:          # 如果 lines 的東西有在 wc
                wc[language] += 1       # wc  就+1
            # else:                     # 取消是因為有自行建立字典會在裡面篩選
            #   wc[lines] = 1           # 不然就初值為1

    except:
        # print(url)              # print 出有問題的網頁
        pass                      # 有些網頁有問題跳過所以pass


######### 內文thread
class getinnerThread(threading.Thread):
    def __init__(self,inner):
        threading.Thread.__init__(self)
        self.inner = inner
    def run(self):                       # run inner
        getinner(self.inner)
        print(self.inner)


#===============================================================
wc = Counter()                           # local variable 'wc' referenced before assignment  要注意區域變數問題！！！  不能放在迴圈
wc["C"] = 0                              # 自行建立字典過濾非必要的單字
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
wc["CSS"] = 0
wc["BASH"] = 0
wc["RUBY"] = 0
wc["PERL"] = 0
wc["SCALA"] = 0
wc["SWIFT"] = 0
wc["GO"] = 0
wc["DELPHI"] = 0
wc["TYPESCRIPT"] = 0

threads = []                            # 標題頁
for i in range(1, 45):                   # 頁數
    Thread = getlinkThread(i)           # 載入頁數中的標題頁
    threads.append(Thread)              # 裝到list裡面
for i in threads:                       # 跑
    i.start()
    time.sleep(0.1)
for i in threads:                       # 等star動作結束在繼續下一步
    i.join()

threadinner = []                        # 內文頁
for inner in links_al:                  # '標題頁links_al' 裡的內文
    Thread = getinnerThread(inner)
    threadinner.append(Thread)
for i in threadinner:
    i.start()
    time.sleep(0.1)
for i in threadinner:
    i.join()
#=======================================================
with open ('../data/518_wei.csv','w') as fw:   # 寫入檔案

    for lang,counts in wc.most_common():
        fw.write('{},{}\n'.format(lang,counts))


#========================================================
import json
from collections import OrderedDict
language = OrderedDict(wc.most_common())
print(language)

# with open('../data/518_wei.json','w') as f:   # 寫入json檔案
#     json.dump(language,f)                    # json 特有
# f.closed
# print (wc.most_common())

# f = open("../data/518_wei.csv","w")
# w = csv.writer(f)
# w.writerows(wc.most_common)
# f.close()


#  圖
import numpy as np
import matplotlib.pyplot as plt

xticks = np.arange(len(language))
plt.xticks(xticks, list(language.keys()))  # 預設 X 座標數字，改顯示水果名
plt.bar(xticks,language.values(),align = 'center')
plt.xticks(rotation = 65)                  #選轉角度
plt.title("language: %d" % len(language))  # 給標題
plt.show()

print('case:'+str(all_case))




