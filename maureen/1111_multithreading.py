import requests    #起手式
from bs4 import BeautifulSoup
import re
from collections import Counter
import matplotlib.pyplot as pt
import numpy as np
import threading
Host = 'https://www.104.com.tw'
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
wc["BASH"] = 0
wc["RUBY"] = 0
wc["PERL"] = 0
wc["SCALA"] = 0
wc["SWIFT"] = 0
wc["GO"] = 0
wc["DELPHI"] = 0
wc["TYPESCRIPT"] = 0
wc["MYSQL"] = 0
wc["FTP"] = 0
wc["DNS"] = 0



def popu(g):  # 此方法是為了取出內頁並且比對內文是否符合要篩選的字
    sk = requests.get(g)
    BS = BeautifulSoup(sk.text, 'lxml')
    data = BS.find('div', {'id': 'midblock'})
    words = data.find_all('dd')  # 抓出專長頁&工作內容也有可能出現語言的需求

    p = re.compile('[A-Z]+[+#]*')  # 正規化
    cols = p.findall(str(words).upper())  # (R) 利用str(words) 改變型態就可以使用upper()

    W = []
    for w in cols:  # 比對出現在頁面中的英文是否出現過 （刪除重複）
        if w not in W:
            W.append(w)

        for c in W:  # 如果有出現在字典中 丟到wc做計算
            if c in wc:
                wc[c] += 1
    #return (wc)








def pagechange(p, wc):  # 此方法是為了取出主頁
    url = "https://www.1111.com.tw/job-bank/job-index.asp?si=1&ss=s&d0=140200,140100,140300,140400&page="
    pages = url + str(p)  # 換頁
    res = requests.get(pages)
    soup = BeautifulSoup(res.text, 'lxml')
    buttons = soup.select('div.jbInfoin > h3 > a')
    link = []
    for i in buttons:
        link.append("https:" + i['href'])
    for i in link:
        popu(i)  # 呼叫popu 方法並把每一內頁代入


def multithreading():
    print(threading.active_count())  # 有幾條執行緒
    print(threading.enumerate())  # 有那幾條執行緒
    print(threading.current_thread())  # 現在是那一條執行緒

    threads = []  # 把所有執行緒都放入列表中
    for i in range(1, 2):  # 利用i取出每一執行緒
        t = threading.Thread(target=pagechange, args=(i, wc))  # 執行方法homepage,args=(要放進方法裡的值,回傳的參數（不一定要用Queue）)
        # pagechange在這裡只是索引值,參數是放在args裡
        t.start()  # 開始執行
        threads.append(t)  # 把執行緒逐一放入列表中
        print('success')
    for thread in threads:
        thread.join()  # 確保執行緒都會先被執行
        print('success1')


if __name__ == '__main__':
    multithreading()  # main下執行

print("DONE!")




leng = []  # 取出每個key
for i in wc.keys():
    leng.append(i)

count = []  # 取出每個 value
for i in wc.values():
    count.append(i)
language = np.arange(len(leng))  # 利用arange產生leng的索引值
for i in wc.keys():
    leng.append(i)
print(leng)
pt.figure(figsize=(18, 5))  # 設定x,y軸寬度
pt.bar(language, count)
pt.xticks(language, leng)
# pt.xticks(rotation=90)
# pt.plot(language, count, linewidth=1)
# pt.ylim(0,800)
pt.title('Language Data Form 1111')
pt.show()



#import json
#with open ('1111_multithreading.json','w') as f:#建json檔
 #   json.dump(wc, f)



with open ('1111_multithreading.csv','w') as fw:   # 寫入檔案
    for lang,counts in wc.most_common():
        fw.write('{},{}\n'.format(lang,counts))
print(wc.most_common())