
# -*- coding: utf-8 -*-

import requests 
from lxml import html 
import os 
import time 
from multiprocessing import Queue,Process
# from Queue import Empty as QueueEmpty
from pymongo import MongoClient 
from datetime import datetime 
from bson.objectid import ObjectId
from threading import Thread

class Douban: 
    
    def __init__(self): 
        """ 连接MongoClient 由3种方法可以选择，看使用情况 """ 
        self.client = MongoClient() 
        # # 指定端口和地址 
        # # self.client = MongoClient('127.0.0.1', 27017) 
        # # 使用URI # self.client = MongoClient('mongodb://127.0.0.1:27017/')

# 选择数据库
        self.db = self.client['Douban']

    def add_one(self, comment, created_time=datetime.now()):
        """
        添加一条数据
        需要注意的是Mongo中不需要事先建立表，插入数据的同时直接根据所传入字典对象的内容生成表
        """
        return self.db.douban.comment.insert_one(comment)

    def find_by_id(self, post_id):
        """
        通过ID查找数据
        Mongo中自动生成的ID主键是ObjectId(id)的形式，所以在查询的时候要遵循该格式
        从bson.objectid导入ObjectId
        """
        return self.db.blog.post.find_one({'_id': ObjectId(post_id)})

    def update_number(self, post_id, number):
        """
        更新一条数据
        在update_one函数中，通过第一个参数查找更新对象，通过第二个参数对查找到的对象进行更新
        下面语句的含义是对指定ID的数据的number字段加上一个number值,通过 $inc 实现
        """
        return self.db.blog.post.update_one({'_id': ObjectId(post_id)}, {'$inc': {'number': number}})

    def update_all_number(self, number):
        """
        批量更新
        update_many函数参数的作用同update_one
        {} 表示没有查找限制，更新全部的数据
        """
        return self.db.blog.post.update_many({}, {'$inc': {'number': number}})

    def delete_by_id(self, post_id):
        """
        根据ID删除，同样注意id值的格式
        """
        return self.db.blog.post.delete_one({'_id': ObjectId(post_id)})





headers = {
      
   'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'zh-CN',
   'Connection': 'Keep-Alive',
   'Cookie': '__utmc=30149280; ck=qByS; ll=108306; bid=z-UccixREcw; __utma=30149280.1468036556.1525396587.1525396587.1525396587.1; __utmz=30149280.1525396587.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2=159906145:u97NJZY/BBk; push_noty_num=0; push_doumail_num=0; __utmv=30149280.15990; as=https://www.douban.com/; ps=y; _vwo_uuid_v2=D23B374E24C7FC61BD8C2E29870ED8FD2|2794ca4eb6acdc787b466fac1ec0e710; __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1525397376%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fsource%3Dsuggest%26q%3D%25E5%2590%258E%25E6%259D%25A5%25E7%259A%2584%25E6%2588%2591%25E4%25BB%25AC%22%5D; _pk_id.100001.4cf6=240ca18d8081420c.1525397376.1.1525397463.1525397376.; __utma=223695111.279609732.1525397376.1525397376.1525397376.1; __utmz=223695111.1525397376.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __yadk_uid=9wXizEZHDhTixFkqMGzxzCCTZsBgw3XM',
   'Host': 'movie.douban.com',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
    }


# 获取主页列表
def getPage(queue):
    
    for i in range(2500):
        baseUrl = 'https://movie.douban.com/subject/26683723/comments?start={}&limit={}&sort=new_score&status=P&percent_type='.format(i*20,(i+1)*20)
        selector = html.fromstring(requests.get(baseUrl,headers=headers).content)
        for i,j in enumerate(selector.xpath('//div[@class="comment"]')):
            votes = j.xpath('//span[@class="comment-vote"]/span/text()')[i]
            comment = j.xpath('//p[@class=""]/text()')[i]
            rating = j.xpath('//span[@class="comment-info"]/span[2]/@class')[i][7:8]
            comments_item = {'vote': votes,
            'comment': comment,
            'rating':rating
            }
            print(comments_item)
            queue.put(comments_item)
            time.sleep(0.5)
    return

def get_values(queue,douban_mongo):
    while True:
        try:
            value = queue.get(True, 10)
        except Exception:
            print("something is wrong")
            continue
        douban_mongo.add_one(value)




if __name__ == '__main__': 
    queue = Queue()
    douban_mongo = Douban()
    getter_process = Thread(target=getPage, args=(queue,))
    
    putter_process = Thread(target=get_values, args=(queue,douban_mongo,))
    getter_process.start()
    putter_process.start()
    