import scrapy
from scrapy import cmdline
import sys
# import pandas as pd
sys.stdout = open('output.txt','wt')

class PhishingWebsitesCrawler(scrapy.Spider):
    '''
        Phishtank phishing website crawler
    '''
    name = 'phishing_websites_crawler'
    allowed_domains = ['phishtank.org']
    start_urls = ['https://phishtank.org/phish_search.php?verified=u&active=y']
    limit = 1
    phishing_website_count = 0

    def parse(self, response):
        # websites_list = response.xpath('//div[@id="main"]//div//div//table[@class="data"]//tbody')
        websites_list = response.xpath('//*[@class="data"]')
        print("**********************************   aaya    ***************************************")
        print("websites_list: ", len(websites_list))

        for i, row in enumerate(websites_list.xpath('tr')):
            if i==0:
                continue
            print(i,"   ---->   ", row.xpath('td[1]//a//@href').extract_first())
        
        for i, row in enumerate(websites_list.xpath('td[5]')):
            print(i,"   ---->   ", row.xpath('b//a//@href').extract_first())

    
    # def parse_phishing_webpage(self, response):
    #     pass
