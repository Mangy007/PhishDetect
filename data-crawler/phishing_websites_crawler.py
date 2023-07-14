import scrapy
import sys
import pandas as pd
import urllib3
sys.stdout = open('output.txt','wt')

base_url = 'https://phishtank.org/'
phishing_website_count = 0
# http = urllib3.PoolManager()

class PhishingWebsitesCrawler(scrapy.Spider):
    '''
        Phishtank phishing website crawler
    '''
    name = 'phishing_websites_crawler'
    allowed_domains = ['phishtank.org']
    start_urls = ['https://phishtank.org/phish_search.php']
    # start_urls = ['https://phishtank.org/user_submissions.php?username=carlittle']
    limit = 100
    data = []
    url_forwarding_base_url = 'https://phishtank.org/phish_search.php'


    def parse(self, response):
        # websites_list = response.xpath('')
        print("**********************************   aaya    ***************************************")
        # print("websites_list: ", len(websites_list))
        print("start limit: ", self.limit)
        print("resp: ", response.xpath('//*[@class="data"]//td[5]//b//a//@href').extract_first())
        # next_page_url = self.start_urls[0]
        # print('------> ', next_page_url)

        if self.limit >= 0:
            print("limit: ", self.limit)
            websites_list = response.xpath('//*[@class="data"]')
            print("websites_list: ", len(websites_list.xpath('tr')))
            for i, row in enumerate(websites_list.xpath('tr')):
                if i==0:
                    continue
                id = row.xpath('td[1]/a//text()').extract_first()
                link = row.xpath('td[1]/a//@href').extract_first()
                is_valid_phish = row.xpath('td[4]//text()').extract_first()
                url_link = base_url+link
                print(i,"   ---->   ", id, url_link)
                item = {"id": id, "url": url_link, "is_valid": is_valid_phish}
                self.data.append(item)
                # request = scrapy.Request(url=url_link, callback=self.parse_phishing_details_page, meta={"id": id, "is_valid": is_valid_phish}, errback=lambda err: print('Error', err), headers={('User-Agent', 'Mozilla/5.0')})
                # yield request
            
            self.limit -= 1
            next_page_url = self.url_forwarding_base_url + response.xpath('//*[@class="data"]//td[5]//b//a//@href').extract_first()
            print('------> ', next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    
    # def parse_phishtank_webpage(self, response):
    #     websites_list = response.xpath('//*[@class="data"]')
    #     for i, row in enumerate(websites_list.xpath('tr')):
    #         if i==0:
    #             continue
    #         id = row.xpath('td[1]//a//text()').extract_first()
    #         link = row.xpath('td[1]//a//@href').extract_first()
    #         is_valid_phish = row.xpath('td[4]//text()').extract_first()
    #         # print(i,"   ---->   ", id, link)
    #         url_link = base_url+link
    #         yield scrapy.Request(url=url_link, callback=self.parse_phishing_details_page, meta={"id": id, "is_valid": is_valid_phish})

    
    def parse_phishing_details_page(self, response):
        url_link = response.xpath('//*[@id="widecol"]/div/div[3]/span/b//text()').extract_first()
        id = response.meta.get("id")
        is_valid = response.meta.get("is_valid")

        item = {"id": id, "url": url_link, "is_valid": is_valid}
        self.data.append(item)
        # print(item)

    def closed(self, reason):
        ''' Method called when spider finishes crawling '''
        df = pd.DataFrame(self.data, columns=["id", "url", "is_valid"])
        # df.to_pickle('../dataset/data.pkl')
        df.to_csv('../dataset/phishtank_data_corpus.csv', index=False)
    


    '''
        code commented for extracting page content but due to max phishing websites
        being deactivated the page content was not available.
    '''

    # def parse_phishing_details_page(self, response):
    #     url_link = response.xpath('//*[@id="widecol"]/div/div[3]/span/b//text()').extract_first()
    #     # link = response.xpath('//*[@class="detailtabs"]/a[3]//@href').extract_first()
    #     # url_link = base_url+link
    #     request = scrapy.Request(url=url_link, callback=self.parse_phishing_page_content, 
    #                                 meta={"id": response.meta.get("id"), "url": url_link})
    #     # print("1", response.meta.get("id"), response.meta.get("is_valid"), url_link)
    #     try:
    #         resp = http.request('GET', url_link)
    #         # print("2", response.meta.get("id"), url_link)
    #         if resp.status==200:
    #             yield request
    #         else:
    #             # print("3", response.meta.get("id"), url_link)
    #             pass
    #     except:
    #         # print("4", response.meta.get("id"), url_link)
    #         pass

    #     print()

    
    # def parse_phishing_page_content(self, response):
    #     if(response.status==200):
    #         print("arre waah!", response.body, response.meta.get("id"))
    #     print("aaya", response.meta.get("id"))
    #     pass
