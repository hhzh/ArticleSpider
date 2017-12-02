# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re
import datetime
from ArticleSpider.items import ArticlespiderItem


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.xpath('//div[@id="archive"]/div/div[@class="post-thumb"]/a')
        for post_node in post_nodes:
            img_url = post_node.xpath('img/@src').extract_first("")
            post_url = post_node.xpath('@href').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_imgage_url": img_url},
                          callback=self.parse_detail)

    def parse_detail(self, response):
        item = ArticlespiderItem()
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        create_date = response.xpath(
            '//div[@class="entry-meta"]/p[@class="entry-meta-hide-on-mobile"]/text()').extract_first('')
        create_date = create_date.replace('.', '').strip()
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        tags = response.xpath('//div[@class="entry-meta"]/p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tags = '/'.join(tags)
        author = response.xpath('//div[@class="copyright-area"]/a/text()').extract_first('')
        source_url = response.xpath('//div[@class="copyright-area"]/a/@href').extract_first('')
        content = response.xpath('//div[@class="entry"]').extract_first('')
        share_nums = response.xpath('//a[@class="jiathis_counter_style"]/span/text()').extract_first('0')
        share_nums=int(share_nums)
        vote_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first('0')
        vote_nums=int(vote_nums)
        bookmark = response.xpath('//span[contains(@class,"bookmark-btn")]/h10/text()').extract_first('')
        bookmark_nums = 0
        match_re = re.match('.*?(\d+).*', bookmark)
        if match_re:
            bookmark_nums = int(match_re.group(1))
        comment = response.xpath('//a[@href="#article-comment"]/text()').extract_first('')
        comment_nums = 0
        match_re = re.match('.*?(\d+).*', comment)
        if match_re:
            comment_nums = int(match_re.group(1))
        item['title'] = title
        item['create_date'] = create_date
        item['tags'] = tags
        item['author'] = author
        item['source_url'] = source_url
        item['content'] = content
        item['share_nums'] = share_nums
        item['vote_nums'] = vote_nums
        item['bookmark_nums'] = bookmark_nums
        item['comment_nums'] = comment_nums
        yield item
