import scrapy
import sys
import pandas as pd
import urllib3
sys.stdout = open('output.txt','wt')


class PhishingWebsitesIdCrawler(scrapy.Spider):
    '''
        Phishtank phishing website crawler
    '''
    name = 'phishing_websites_id_crawler'
    allowed_domains = ['phishtank.org']
    start_urls = ['https://phishtank.org/phish_search.php']
    limit = 5000
    data = []
    url_forwarding_base_url = 'https://phishtank.org/phish_search.php'
    base_url = 'https://phishtank.org/'

    custom_settings = {
         'CONCURRENT_REQUESTS' : 500,
         'DOWNLOAD_DELAY' : 2.5
    }


    def parse(self, response):
        if self.limit >= 0:
            websites_list = response.xpath('//*[@class="data"]')
            for i, row in enumerate(websites_list.xpath('tr')):
                if i==0:
                    continue
                id = row.xpath('td[1]/a//text()').extract_first()
                link = row.xpath('td[1]/a//@href').extract_first()
                is_valid_phish = row.xpath('td[4]//text()').extract_first()
                url_link = self.base_url+link
                item = {"id": id, "url": url_link, "is_valid": is_valid_phish}
                self.data.append(item)
            
            self.limit -= 1
            next_page_url = self.url_forwarding_base_url + response.xpath('//*[@class="data"]//td[5]//b//a//@href').extract_first()
            yield scrapy.Request(next_page_url, callback=self.parse)

    

    def closed(self, reason):
        ''' Method called when spider finishes crawling '''
        df = pd.DataFrame(self.data, columns=["id", "url", "is_valid"])
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
