# -*- coding: utf-8 -*-
import scrapy
from items import DemoItem
from urllib.parse import quote
from scrapy import Request, Spider
from bs4 import BeautifulSoup
import json
class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    # allowed_domains = ['www.jd.com']
    base_url = 'https://search.jd.com/Search?keyword='
    def start_requests(self):
        for keyword in self.settings.get("KEYWORDS"):
            for page in range(self.settings.get("MAX_PAGE") + 1):
                # print(page)
                #print(keyword)
                url=self.base_url+quote(keyword)
                #RL只允许一部分ASCII字符，其他字符（如汉字）是不符合标准的，此时就要进行编码
                # print(url)
                yield Request(url=url,callback=self.parse,meta={"page":2},dont_filter=True)
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lis = soup.find_all(name='li', class_="gl-item")
        pass
        for li in lis:
            item=DemoItem()
            id = li.attrs['data-sku']
            item['id']=id
            # color=response.xpath('//div[@id="choose-attr-1"]/div//@data-value').getall()
            # type=response.xpath('//div[@id="choose-attr-2"]/div[@class="dd"]/div/@data-value').getall()
            url = 'https://item.jd.com/' + id + '.html'
            # item['url']=url
            # item['color']=color
            # item['type']=type
            # print(url)
            # print("*"*50)
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={"item":item})
    def parse_detail(self,response):
        print(response.url)
        item = response.meta["item"]
        print("-"*50)
        id = response.xpath('//div[@class="left-btns"]/a/@data-id').get()
        title=response.xpath('//div[@class="sku-name"]//text()').get().strip()
        color=response.xpath('//div[@id="choose-attr-1"]/div//@data-value').getall()
        type=response.xpath('//div[@id="choose-attr-2"]/div[@class="dd"]/div/@data-value').getall()
        item['color']=color
        item['type']=type
        #商品名称
        item['name']=title
    #     #https://club.jd.com/comment/productCommentSummaries.action?referenceIds=8184522
        commend_js="https://club.jd.com/comment/productCommentSummaries.action?referenceIds="+id
        yield scrapy.Request(commend_js,callback=self.parser_json,meta={"item":item})
        #https://p.3.cn/prices/mgets?&skuIds=J_100006946970
        price_js='https://p.3.cn/prices/mgets?&skuIds='+id
        yield scrapy.Request(price_js, callback=self.parser_price, meta={"item": item})
        yield item
    def parser_price(self,response):
        item = response.meta["item"]
        price=json.loads(response.text)[0]['p']
        item['price']=price
        yield item
    #获取评价
    def parser_json(self,response):
        item=response.meta["item"]
        data=json.loads(response.text)["CommentsCount"][0]
        comment_count = data['CommentCountStr']
        item['comment_count']=comment_count
        #总评价
        goodCount = data['GoodCountStr']
        item['goodCount']=goodCount
        #好评
        #中评
        generalCount = data['GeneralCountStr']
        item['generalCount']=generalCount
        #差评
        poorCount=data['PoorCountStr']
        item['poorCount']=poorCount
        yield item

