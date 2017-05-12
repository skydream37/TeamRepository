# from splinter import Browser

# 用 selenium 去爬取  注意： selenium與splinter  是不同東西
from selenium import webdriver
import time
import re
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# ===========================================================================
# 設定進入頁面
host = 'http://www.yes123.com.tw/admin/'
browser = webdriver.Chrome()
browser.get(host + "job_refer_list.asp")

# 進入頁面輸入關鍵字搜尋
browser.find_element_by_id('find_key1').clear()                       # 把欄位清除文字
browser.find_element_by_id('find_key1').send_keys('軟體 工程師')       # 輸入文字
time.sleep(2)
browser.find_element_by_class_name('n_serch_btn').click()             # 搜尋扭
time.sleep(2)
soup = BeautifulSoup(browser.page_source, 'lxml')                     # 所有網頁的原始碼
time.sleep(2)
counter = 0                                                           # 頁數

while True:
    try:
        counter += 1                                                  # 頁數迴圈增加
        eles = []
        for ele in soup.select('a.jobname'):                          # 標題頁網頁連結
            eles.append(host + ele['href'])                           # 把標題頁網頁連結取出用 eles 裝箱

        browser.find_element_by_tag_name('body').send_keys(Keys.END)  # 模擬鍵盤 （end鍵往下捲動）
        time.sleep(0.5)

        with open('link_yes123_test3.csv', 'a') as f:   # 寫入檔案
            f.write('\n'.join(eles) + '\n')             # 回傳將 str 連結 iterable 各元素的字串

        browser.find_element_by_link_text('>').click()  # 點擊按鈕
        time.sleep(1)

    except Exception as e:                              # 固定寫法有問題丟給 e
        print(e)
        break

print('The end of pages is No.%d' % (counter))
print('Browser will quit!')
browser.quit()


# ===================================================================================

# browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')              # 無限捲軸 （josn格式寫法）

# browser.find_element_by_tag_name('body').send_keys(Keys.END)                          # 模擬鍵盤 （end鍵往下捲動）

# ===================================================================================
import requests
from bs4 import BeautifulSoup
from collections import Counter
from collections import OrderedDict
import json
#=====================================================================================
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


def get_inner(open_link):
    try:
        res = requests.get(open_link)
        soup = BeautifulSoup(res.text, 'lxml')

        line1 = soup.select('div.comp_detail > ul > li > .rr')[0].text          # 徵才說明
        line2 = str(soup.select('div.comp_detail > ul > li'))                   # 技能與求職專長(有些會搜尋不到)
        line = line1 + line2
        up = line.upper()                                                       # 統一轉為大寫處理
        line = re.findall('[A-Z]+[+#-C]*', "%s" % up)                           # 正規化處理
        line_c = []                                                             # 給予list 裝單字元素
        for line_a in line:                                                     # 把 line 元素 給予line_a
            if line_a not in line_c:                                            # 如果 line_a 的元素不再 lin_c 裡面
                line_c.append(line_a)                                           # 把 line_a  附加給 lin_c

        for language in line_c:                                                 # 把整理好的line_c 值取出到自定義的 language (list形式)
            if language in wc:                                                  # 如果 lines 的東西有在 wc
                wc[language] += 1                                               # wc  就+1
          # else:                                                               # 取消是因為有自行建立字典會在裡面篩選
               #wc[language] = 1                                                # 不然就初值為1

    except:
        print(open_link)                                                        # print 出有問題的網頁
        pass

#=============================================================================
with open('link_yes123_test3.csv', 'r') as fr:              # 檔案匯入
    for open_link in fr.read().strip().split('\n'):
        get_inner(open_link)                                # 把檔案丟入方法
# print(open_link)

#=============================================================================
language = OrderedDict(wc.most_common())
print(language)

# with open('yes123_json.json', 'w') as fu:   # 寫入json檔案
#     json.dump(language, fu)                 # json 特有
#     fu.closed

with open('yes123_json.json','w') as f:   # 寫入json檔案
    json.dump(wc,f)                    # json 特有
f.closed

print(wc.most_common())