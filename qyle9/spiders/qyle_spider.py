#coding=utf-8
import scrapy
from qyle9.items import Qyle9Item

class QyleSpider(scrapy.Spider):
    name = "qyle9"
    allowed_domains = ["qyle9.com"]
    start_urls =["http://www.qyle9.com/recent/2/"]

    def parse(self , response):
        base = u'http://www.qyle9.com'
        #links = []
        for sel in response.xpath('//div[@class="panel-body panel-padding"]/ul/li'):
            #item = Qyle9Item()
            url = sel.xpath('div/a/@href').extract()
            url = base + url[0]
            self.log(url)
            yield scrapy.Request(url , callback = self.parse_content)
            #links.append(link)
        Page = response.xpath('//div[@class="panel-body panel-padding"]/nav/ul/li/a[@class="prevnext"]/@href').extract()

        nextPage = None
        if len(Page) != 1:
            nextPage = Page[-1]

        if nextPage:
            nextPage = base + nextPage
            self.log(nextPage)
            yield scrapy.Request(nextPage , callback = self.parse)

    def parse_content(self , response):
        item = Qyle9Item()
        #item["link"] = response.xpath('//div[@id="player-container"]/video/source/@src').extract()[0]
        try:
            link = response.xpath('//video[@id="player"]/source/@src').extract()[0]
        except:
            link = ""
        item["link"] = link

        yield item
