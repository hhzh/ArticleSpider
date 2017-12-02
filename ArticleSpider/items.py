# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
import datetime
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def date_covert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def return_value(value):
    return value


def get_nums(value):
    nums = 0
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    return nums

def get_list(value):
    return [value]


class ArticleSpiderItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(return_value)
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_covert)
    )
    tags = scrapy.Field(
        output_processor=Join(',')
    )
    author = scrapy.Field()
    source_url = scrapy.Field()
    content = scrapy.Field()
    share_nums = scrapy.Field(
        input_proecessor=MapCompose(get_nums)
    )
    vote_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    bookmark_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    front_image_url = scrapy.Field()
    article_url = scrapy.Field()
    image_urls=scrapy.Field(
        input_processor=MapCompose(get_list)
    )



class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
