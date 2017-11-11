# -*- coding: utf-8 -*-
import scrapy
import json
import random
from time import sleep
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor



class AppbrainbotSpider(scrapy.Spider):
    name = 'appbrainbot'
    # allowed_domains = ['https://www.appbrain.com']
    start_urls = ['https://www.appbrain.com/apps/highest-rated']

    def __init__(self):

        super().__init__()

        self.app_name = {}
        self.app_count = 0
        self.page_count = 0
        self.site = 'https://www.appbrain.com{0}'

        dispatcher.connect(self.spider_closed,signals.spider_closed)


    def start_requests(self):
        print("start_request")
        yield scrapy.Request(url = self.start_urls[0], callback = self.parse)



    def parse(self, response):

        print("parse")
        print(response.url)
        app = response.css(".browse-app-large.safelink.hover-shadow.hidden-xs::attr(href)").extract()
        print(app)

        for iapp in app:
            print(self.site.format(iapp))
            self.app_count += 1

            yield scrapy.Request(url = self.site.format(iapp).strip(), callback = self.parse_app)

        if self.app_count < 1000:
            print("parse if else")
            self.page_count += 1
            url ="/apps/popular/?o={0}".format(self.page_count * 10)
            yield scrapy.Request(url = self.site.format(url), callback = self.parse)


    def parse_app(self, response):
        print("parse_app")
        #Extrac the name, its returned as a string in a list with one element therefore we
        #slice the string out with [0]
        app_real_name = response.css(".bottommargin-s::text").extract()[0]

        #Extracts the description
        desc = " ".join(response.css(".app-description-contents::text").extract())
        sleep(5)
        self.app_name[app_real_name] = desc


    def spider_closed(self, spider):
        print(self.app_name)
        with open("app_desc.json", "w", encoding = "utf-8") as file:
            json.dump(self.app_name, file)


def main():
    runner = CrawlerRunner()
    d = runner.crawl(AppbrainbotSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == "__main__":
    main()
