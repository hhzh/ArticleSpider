# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class ArticlespiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='article',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # sql='insert into article(title) VALUE (%s)'
        # self.cursor.execute(sql,(item["title"]))
        sql = 'insert into article (title,author,tags,source_url,share_nums,vote_nums,bookmark_nums,comment_nums,create_date,content,article_url,front_image_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        print(item['title'], item['author'], item['tags'], item['source_url'], item['share_nums'], item['vote_nums'],
              item['bookmark_nums'], item['comment_nums'], item['create_date'], item['content'], item['article_url'],item['front_image_url'])
        self.cursor.execute(sql, (
            item['title'], item['author'], item['tags'], item['source_url'], item['share_nums'], item['vote_nums'],
            item['bookmark_nums'], item['comment_nums'], item['create_date'], item['content'], item['article_url'],item['front_image_url']))
        self.conn.commit()
        return item

    def spider_closed(self, spider):
        self.conn.close()
