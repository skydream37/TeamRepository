
# coding: utf-8

import requests
import datetime, time
import jieba
from wordcloud import WordCloud
import string
import matplotlib.pyplot as plt

class FBAPI():
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v2.5/"
        self.set_since_time()
        self.set_until_time()
        pass

    def login(self, token):
        self.token = token
        #test login
        qs = {"fields":"id,name",
              "access_token":self.token}
        info = self.make_request("me", qs)
        if "id" in info and "name" in info:
            print("Your ID   : ", info["id"])
            print("User Name : ", info["name"])
            self.id = info["id"]
            self.name = info["name"]
            self.is_login = True
        else:
            print("Login Failed")

    def make_request(self, url, qs={}):
        while True:
            try:
                x = requests.get(self.base_url+url, params=qs)
                response = x.json()
                return response
            except requests.exceptions.ConnectionError:
                print( "Internet sucks" )

    def request(self, url):
        while True:
            try:
                x = requests.get(url)
                response = x.json()
                return response
            except requests.exceptions.ConnectionError:
                print( "Internet sucks" )

    #"https://graph.facebook.com/v2.5/me/posts"
    def get_posts(self):
        qs = {"fields":"id, message",
              "since":self.since_time,
              "until":self.until_time,
              "access_token":self.token}
        url = "me/posts/"
        response = self.make_request(url, qs)

        if "data" not in response:
            print("Posts Not Found")
            return []

        posts = response["data"]
        while "paging" in response and "next" in response["paging"]:
            response = self.request(response["paging"]["next"])
            if "data" in response:
                posts.extend(response["data"])
        print("get ", len(posts), " posts")
        posts = list(map(lambda x:x["id"], posts))
        return posts

    def get_post( self , post_id ):
        qs = {
            "fields": "message",
            "access_token": self.token
        }
        response = self.make_request( post_id , qs )
        if "message" not in response:
            return ''
        return response[ 'message' ]

    #Year-Month-Day
    def set_since_time(self, since_time = "2000-01-01"):
        self.since_time = int(time.mktime(datetime.datetime.strptime(since_time, "%Y-%m-%d").timetuple()))

    def set_until_time(self, until_time = "2020-01-01"):
        self.until_time = int(time.mktime(datetime.datetime.strptime(until_time, "%Y-%m-%d").timetuple()))

    def get_sprout_posts(self):
        qs = {"fields":"message, created_time, likes.summary(true)",
              "since":self.since_time,
              "until":self.until_time,
              "access_token":self.token}
        response = self.make_request('109294965910483/posts', qs)

        if "data" not in response:
            print("Posts Not Found")
            return []
        posts = response["data"]

        while "paging" in response and "next" in response["paging"]:
            response = self.request(response["paging"]["next"])
            if "data" in response:
                posts.extend(response["data"])
        print("get ", len(posts), " posts")
        posts = list(map(lambda x:x["id"], posts))
        return posts

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕】〞︰︱︳﹐､﹒
            ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
            々∥•‧ˇˉ─--′』」([{£¥'"‵〈《「『【〔【（［｛￡￥〝︵︷︹︻
            ︽︿﹁﹃﹙﹛﹝（｛「『-—_…''')

punct.union( string.punctuation )
punct.union( string.whitespace )

def get_words( post ):
    raw_words = jieba.lcut( post )
    return list( filter( lambda s:s not in punct , raw_words ) )

def draw_word_cloud( freq_list , file_name='word_cloud.png' ):
    # Generate a word cloud image
    wordcloud = WordCloud(
        font_path='NotoSansCJKtc-Regular.otf',
        width=960,
        height=480,
        relative_scaling=.5
    ).generate_from_frequencies( freq_list )
    wordcloud.to_file( file_name )

def draw_word_cloud_jupyter( freq_list ):
    # Generate a word cloud image
    wordcloud = WordCloud(
        font_path='NotoSansCJKtc-Regular.otf',
        width=720,
        height=360,
        relative_scaling=.5
    ).generate_from_frequencies( freq_list )
    # the matplotlib way:
    get_ipython().magic(u'matplotlib inline')
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

