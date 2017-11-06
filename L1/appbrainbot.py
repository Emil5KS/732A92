# -*- coding: utf-8 -*-
import scrapy


class AppbrainbotSpider(scrapy.Spider):
    name = 'appbrainbot'
    allowed_domains = ['https://www.appbrain.com/apps/highest-rated']
    start_urls = ['http://https://www.appbrain.com/apps/highest-rated']
    my_urls = []
    app_name = []

    
    def parse(self, response):

        #There might be a "/" between the "..com" and the "{0}"
        site = 'https://www.appbrain.com{0}'
        app = response.css(".browse-app-large.safelink.hover-shadow.hidden-xs::attr(href)").extract() 

        url_app = []  #List of urls with apps
        desc = [] # A list where each element consists of a list which is the description for each app.
        
        for iapp in app:
            url_app.append() = site.format(iapp)

        #while len(url_app) < 1000:
         for url in url_app:
             
             if next_page is not None:
                yield response.follow(next_page, self.parse)

             #Extrac the name, its returned as a string in a list with one element therefore we
                #slice the string out with [0]
             app_name.append(response.css(".bottommargin-s::text").extract()[0])
             
             #Extracts the description 
             desc.append(response.css(".app-description-contents::text").extract())

             # This is a list of new links to other apps from the app description page.
             new_app = response.css(".app-tile.hover-shadow::attr(href)").extract():

             # Adds these new url's in to the url_app list.
              
             for new_links in new_app:                 
                 url_app.append(stie.format(new_link))

             # The question now is, will all the url's be unique? Should we do set() on the url
             # or how should we do it? If we use set i assume the url_app would be scrambled
             # since set is not sorted. This would lead to us maybe visiting the same page twice and therefore
             # creating duplicates.

             
             
             


 

        pass
