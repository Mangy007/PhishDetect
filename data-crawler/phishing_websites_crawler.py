import scrapy
from scrapy import cmdline
# import pandas as pd

class PhishingWebsitesCrawler(scrapy.Spider):
    '''
        Phishtank phishing website crawler
    '''
    name = 'phishing_websites_crawler'
    allowed_domains = ['phishtank.org']
    start_urls = ['https://phishtank.org/phish_search.php?verified=u&active=y']
    limit = 1000
    phishing_website_count = 0

    def parse(self, response):
        # websites_list = response.xpath('//div[@id="main"]//div//div//table[@class="data"]//tbody')
        websites_list = response.xpath('//*[@class="data"]//tr')
        print("**********************************   aaya    ***************************************")
        print("websites_list: ", len(websites_list))

        for i, row in enumerate(websites_list[1].xpath('//td[1]//@href')):
            if i==0:
                continue
            # id = row.xpath('//td[1]//@href')
            # print(i,"   ---->   ", row.xpath('//td[1]//text()'))
            print(i, " --- ", row)
    
    # def parse_phishing_webpage(self, response):
    #     pass
