import scrapy
import pandas as pd

class PhishingWebsitesCrawler(scrapy.Spider):
    name = 'phishing_websites_crawler'
    allowed_domains = ['phishtank.org']
    start_urls = ['https://phishtank.org/phish_search.php?verified=u&active=y']

    def parse(self, response):
        websites_list = response.xpath('//div[@id="main"]//table[@class="data"]//tbody')
        websites = []

        flag = True
        i = 0
        for website in websites_list:
            if i==10:
                break
            if flag:
                continue
            else:
                print(website)
            flag =  False
            i += 1
    
