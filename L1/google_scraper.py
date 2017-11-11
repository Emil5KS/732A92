



# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class AppbrainbotSpider(scrapy.Spider):
    name = 'appbrainbot'
    # allowed_domains = ['https://www.appbrain.com']
    start_urls = ['https://play.google.com/store/apps/category/PERSONALIZATION/collection/topselling_free']

    def __init__(self):

        super().__init__()

        self.apps = {}
        self.apps_url = []
        self.app_count = 0
        #self.page_count = 0
        self.site = "https://play.google.com/store/apps/category/{0}/collection/topselling_free"
        self.cats = ["COMMUNICATION","PHOTOGRAPHY", "LIFESTYLE", "PRODUCTIVITY", "SPORTS", "TOOLS”,”ANDROID_WEAR","EVENTS","BUSINESS", "HEALTH_AND_FITNESS"]

        dispatcher.connect(self.spider_closed,signals.spider_closed)


    def start_requests(self):
        print("start_request")
        yield scrapy.Request(url = self.start_urls[0], callback = self.parse)



    def parse(self, response):

        print("parse")
        print(response.url)
        urls = response.css(".title::attr(href)").extract()

        for url in urls:

            self.app_count += 1
            complete_url = self.site.format(url)
            print(complete_url)
            self.app_url.append(complete_url)

            # this is a pretty stupid logical statement to solve it with since we
            # can scrape the same app twice and therefor land below 1000, but its ok.
        if self.app_count < 1000:
            print("parse if else")
            for category in self.cats:
                #self.page_count += 1
                getting_new_urls = self.site.format(category)
                yield scrapy.Request(url = getting_new_urls, callback = self.parse)


        for iapp in app:
            print(self.site.format(iapp))
            self.app_count += 1
            yield scrapy.Request(url = self.site.format(iapp).strip(), callback = self.parse_app)






    def parse_app(self, response):
        print("parse_app")
        #Extrac the name, its returned as a string in a list with one element therefore we
        #slice the string out with [0]
        app_real_name = response.css(".bottommargin-s::text").extract()[0]

        #Extracts the description
        desc = " ".join(response.css(".app-description-contents::text").extract())

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
