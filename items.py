# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()

    price = scrapy.Field()
    color = scrapy.Field()
    type = scrapy.Field()
    id=scrapy.Field()
    # type = scrapy.Field()
    comment_count=scrapy.Field()
    goodCount=scrapy.Field()
    generalCount=scrapy.Field()
    poorCount=scrapy.Field()
    # dp = scrapy.Field()
    # title = scrapy.Field()
    # price = scrapy.Field()
    # comment = scrapy.Field()
    url = scrapy.Field()


