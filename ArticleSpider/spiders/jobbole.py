# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re
import datetime
from ArticleSpider.items import ArticleSpiderItem, ArticleItemLoader
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.xpath('//div[@id="archive"]/div/div[@class="post-thumb"]/a')
        for post_node in post_nodes:
            img_url = post_node.xpath('img/@src').extract_first("")
            post_url = post_node.xpath('@href').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": img_url},
                          callback=self.parse_detail)

        next_url = response.xpath(
            '//div[contains(@class,"navigation")]/a[contains(@class,"next")]/@href').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # item = ArticlespiderItem()
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        # create_date = response.xpath(
        #     '//div[@class="entry-meta"]/p[@class="entry-meta-hide-on-mobile"]/text()').extract_first('')
        # create_date = create_date.replace('·', '').strip()
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # tags = response.xpath(
        #     '//div[@class="entry-meta"]/p[@class="entry-meta-hide-on-mobile"]/a[contains(@href,"tag")]/text()').extract()
        # tags = '/'.join(tags)
        # author = response.xpath('//div[@class="copyright-area"]/a/text()').extract_first('')
        # source_url = response.xpath('//div[@class="copyright-area"]/a/@href').extract_first('')
        # content = response.xpath('//div[@class="entry"]').extract_first('')
        # share_nums = response.xpath('//a[@class="jiathis_counter_style"]/span/text()').extract_first('0')
        # share_nums = int(share_nums)
        # vote_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first('0')
        # vote_nums = int(vote_nums)
        # bookmark = response.xpath('//span[contains(@class,"bookmark-btn")]/h10/text()').extract_first('')
        # bookmark_nums = 0
        # match_re = re.match('.*?(\d+).*', bookmark)
        # if match_re:
        #     bookmark_nums = int(match_re.group(1))
        # comment = response.xpath('//a[@href="#article-comment"]/text()').extract_first('')
        # comment_nums = 0
        # match_re = re.match('.*?(\d+).*', comment)
        # if match_re:
        #     comment_nums = int(match_re.group(1))

        # item['title'] = title
        # item['create_date'] = create_date
        # item['tags'] = tags
        # item['author'] = author
        # item['source_url'] = source_url
        # item['content'] = content
        # item['share_nums'] = share_nums
        # item['vote_nums'] = vote_nums
        # item['bookmark_nums'] = bookmark_nums
        # item['comment_nums'] = comment_nums
        # item['front_image_url'] = front_image_url
        # item['article_url']=response.url

        front_image_url = response.meta.get('front_image_url', '')
        image_urls = response.meta.get('front_image_url', [])

        item_loader = ArticleItemLoader(item=ArticleSpiderItem(), response=response)
        item_loader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('create_date', '//div[@class="entry-meta"]/p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_xpath('tags',
                              '//div[@class="entry-meta"]/p[@class="entry-meta-hide-on-mobile"]/a[contains(@href,"tag")]/text()')
        item_loader.add_xpath('author', '//div[@class="copyright-area"]/a/text()')
        item_loader.add_xpath('source_url', '//div[@class="copyright-area"]/a/@href')
        item_loader.add_xpath('content', '//div[@class="entry"]')
        item_loader.add_xpath('share_nums', '//a[@class="jiathis_counter_style"]/span/text()')
        item_loader.add_xpath('vote_nums', '//span[contains(@class,"vote-post-up")]/h10/text()')
        item_loader.add_xpath('bookmark_nums', '//span[contains(@class,"bookmark-btn")]/h10/text()')
        item_loader.add_xpath('comment_nums', '//a[@href="#article-comment"]/text()')
        item_loader.add_value('front_image_url', front_image_url)
        item_loader.add_value('article_url', response.url)
        item_loader.add_value('image_urls', image_urls)
        item = item_loader.load_item()
        yield item
