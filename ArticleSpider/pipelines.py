# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline

class ArticlespiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='article',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, '')
        sql = 'insert into article (title,author,tags,source_url,share_nums,vote_nums,bookmark_nums,comment_nums,create_date,content,article_url,front_image_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        print(item['title'], item['author'], item['tags'], item['source_url'], item['share_nums'], item['vote_nums'],
              item['bookmark_nums'], item['comment_nums'], item['create_date'], item['article_url'],
              item['front_image_url'])
        self.cursor.execute(sql, (
            item['title'], item['author'], item['tags'], item['source_url'], item['share_nums'], item['vote_nums'],
            item['bookmark_nums'], item['comment_nums'], item['create_date'], item['content'], item['article_url'],
            item['front_image_url']))
        self.conn.commit()
        return item

    def spider_closed(self, spider):
        self.conn.close()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        for field in item.fields:
            item.setdefault(field, '')
        sql = 'insert into article (title,author,tags,source_url,share_nums,vote_nums,bookmark_nums,comment_nums,create_date,content,article_url,front_image_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['title'], item['author'], item['tags'], item['source_url'], item['share_nums'], item['vote_nums'],
            item['bookmark_nums'], item['comment_nums'], item['create_date'], item['content'], item['article_url'],
            item['front_image_url']))

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        pass