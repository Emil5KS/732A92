# -*- coding: utf-8 -*-
import scrapy
import json
import random
from time import sleep
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

class GooglePlaySpider(scrapy.Spider):
    name = 'googleplay_bot'
    allowed_domains = ['play.google.com']

    def __init__(self):
        super().__init__()

        self.app_name_desc = {}

        self.base_url = "https://play.google.com"
        self.base_category_url = self.base_url + "/store/apps/category/%s/collection/topselling_free"
        self.english_language_specifier_site = "?hl=en"
        self.english_language_specifier_app = "&hl=en"

        self.categories = ["EDUCATION", "MEDICAL", "DATING", "COMMUNICATION",
                           "FINANCE", "HEALTH_AND_FITNESS",
                           "MUSIC_AND_AUDIO", "PERSONALIZATION", "ENTERTAINMENT",
                           "EVENTS", "COMICS", "BEAUTY", "LIFESTYLE", "MAPS_AND_NAVIGATION",
                           "HOUSE_AND_HOME", "BUSINESS", "BOOKS_AND_REFERENCES", "ART_AND_DESIGN",
                           "FOOD_AND_DRINK", "ANDROID_WEAR", "GAME_ACTION", "GAME_ADVENTURE"]

        self.apps_visited = set()
        self.max_apps = 1500
        self.app_xpath = "//a[@class='card-click-target']/@href"

        self.app_name_xpath = "//div[@class='id-app-title']/text()"
        self.app_desc_xpath = "//div[@itemprop='description']/div/text()"

        dispatcher.connect(self.spider_closed,signals.spider_closed)


    def start_requests(self):
        print("Start Requests")

        for category in self.categories:
            url = self.base_category_url % category + self.english_language_specifier_site
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        print("Parsing", response.url)

        app_urls = set(response.xpath(self.app_xpath).extract())

        for app_url in app_urls:
            url = self.base_url + app_url + self.english_language_specifier_app

            if url not in self.apps_visited and len(self.apps_visited) < self.max_apps:
                self.apps_visited.add(url)
                yield scrapy.Request(url=url, callback=self.parse_app)

    def parse_app(self, response):
        print("Parsing app", response.url)

        name = " ".join(response.xpath(self.app_name_xpath).extract())
        desc = " ".join(response.xpath(self.app_desc_xpath).extract())

        self.app_name_desc[name] = desc

    def spider_closed(self, spider):
        print(len(self.app_name_desc))
        with open("app_desc.json", "w", encoding = "utf-8") as file:
            json.dump(self.app_name_desc, file)


def main():
    runner = CrawlerRunner()
    d = runner.crawl(GooglePlaySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == "__main__":
    main()
