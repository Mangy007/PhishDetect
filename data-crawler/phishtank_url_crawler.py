import scrapy
import pandas as pd


def get_urls_from_csv():
    df = pd.read_csv('../dataset/phishtank_data_corpus.csv')
    return df['url'].to_list()

class PhishtankURLCrawler(scrapy.Spider):
    '''
        Phishtank phishing website url crawler
    '''
    name = 'phishtank_url_crawler'
    allowed_domains = ['phishtank.org']
    data = []

    custom_settings = {
         'CONCURRENT_REQUESTS' : 500,
         'DOWNLOAD_DELAY' : 1,
         'RANDOMIZE_DOWNLOAD_DELAY': False
    }

    def start_requests(self):
        return [scrapy.http.Request(url=start_url) for start_url in get_urls_from_csv()]


    def parse(self, response):

        url_link = response.xpath('//*[@id="widecol"]/div/div[3]/span/b//text()').extract_first()
        id = int(response.xpath('//*[@id="widecol"]/div/h2//text()').extract_first().split()[-1][1:])
        time = " ".join(response.xpath('//*[@id="widecol"]//div[@class="url"]/span//text()').extract_first().split()[1:][:-1])

        item = {"id": id, "phishing_url": url_link, "submission_time": time}
        self.data.append(item)


    def closed(self, reason):
        ''' Method called when spider finishes crawling '''
        df_1 = pd.DataFrame(self.data, columns=["id", "phishing_url", "submission_time"])
        df = pd.read_csv('../dataset/phishtank_data_corpus.csv')
        df = df.merge(df_1, how='inner', on='id')
        df.to_csv('../dataset/phishtank_data_corpus_new.csv', index=False)
    
