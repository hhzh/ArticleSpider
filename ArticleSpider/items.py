# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    create_date = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()
    source_url = scrapy.Field()
    content = scrapy.Field()
    share_nums = scrapy.Field()
    vote_nums = scrapy.Field()
    bookmark_nums = scrapy.Field()
    comment_nums = scrapy.Field()