import scrapy
import csv
import pandas as pd
import os
import numpy as np

from scrapy.crawler import CrawlerProcess
headers = {
'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}
def processing(data):
    for index in range(len(data)-1):
        modified = str(data[index]).split("'")
        data[index] = modified[1]
        if modified[1].find("Rs") >= 0:
            hello = data[index].split("Rs")
            temp = hello[1]
            temp = (temp.strip('.')).strip(' ')
            temp = temp.replace(',', "")
            data[index] = int(float(temp))
    return data


class ProductsSpider(scrapy.Spider):
    name = "gaming"
    output = 'example.csv'

    def __init__(self):
        file = open('example.csv', "w")

    def start_requests(self):
        #product = input("Enter the item you are looking for")
        product = 'mouse'
        urls = [#f'https://www.czone.com.pk/search.aspx?kw={product}',
                f'https://pcfanatics.pk/search?type=product&q={product}',
                #f'https://www.eezepc.com/?s={product}&post_type=product',
                f'https://www.industech.pk/search/?kw={product}',
                f'https://rbtechngames.com/?s={product}&product_cat=0&post_type=product',
                f'http://www.gtstore.pk/searchresults.php?inputString={product}&x=0&y=0'
             ]
        for URL in urls:
            yield scrapy.Request(
                url = URL,
                callback=self.parse,
                headers = headers)

    def parse(self, response):
        '''
        if response.css('title::text').get().find("Computer Zone Pakistan")>=0:
            yield{
                'title': response.css('.col-lg-8.col-md-8.col-sm-8.col-xs-12 h4 a::text').get(),
                'website' : "www.czone.com.pk",
                'price' : response.css('span#rptListView_ctl00_spnPrice::text').extract(),
                'rating': response.css('span.product-rating::text').extract()[0],
            }
            url = response.css('.col-lg-8.col-md-8.col-sm-8.col-xs-12 h4 a::attr(href)').get()
            comp_url = response.urljoin(url)
            extra = yield scrapy.Request(url=url, callback=self.parse2, headers=headers)
            thread = threading.Thread(target=extra)
            thread.start()

        elif response.css('title::text').get().find('EEZEPC') >= 0 :
            yield {
                'title' : response.css('.woocommerce-loop-product__title::text').get(),
                'website' : "www.eezepc.com",
                'price' : response.css('span.woocommerce-Price-amount.amount>bdi::text').get().strip()
            }
            url = response.css('div.product-inner a::attr(href)').extract()[0].strip()
            extra = yield scrapy.Request(url=url, callback=self.parse2, headers=headers)
            thread = threading.Thread(target=extra)
            thread.start()
        '''
        with open(self.output,"a",newline="") as f:
            writer = csv.writer(f)
            if response.css('title::text').get().find("PC Fanatics") >= 0:
                title = response.css('.productitem--title a::text').get().strip(),
                website = "www.pcfanatics.pk",
                price = response.css('span.money::text').get().strip(),
                rating = "'Not available'",
                review = "'None'"
                image = response.css('img.productitem--image-primary::attr(src)').get()
                clean_img = '\'' + response.urljoin(image) + '\''
                writer.writerow(processing([title,website,price,rating,review,clean_img]))
            elif response.css('title::text').get().find("IndusTech") >= 0:
                title = response.css('a#rptListView_ctl00_anProductName::text').get(),
                website = "www.industech.pk",
                price = response.css('span#rptListView_ctl00_spnPrice::text').get(),
                rating = "'None'",
                review = "'None'"
                image = response.css('img#rptListView_ctl00_imgProduct::attr(src)').get()
                clean_img = '\'' + response.urljoin(image) + '\''
                writer.writerow(processing([title, website, price, rating, review, clean_img]))
            elif response.css('title::text').get().find('RB Tech') >= 0:
                title = response.css('.woocommerce-loop-product__title::text').get(),
                website= 'www.rbtechngames.com',
                price = "Rs." + response.css('span.woocommerce-Price-amount.amount>bdi::text').getall()[1],
                rating = "'None'",
                review = "'None'"
                image = response.css('img.attachment-woocommerce_thumbnail.size-woocommerce_thumbnail::attr(src)').get()
                clean_img = '\''+ response.urljoin(image) + '\''
                writer.writerow(processing([title, website, price, rating, review, clean_img]))
            elif response.css('title::text').get().find('GT') >= 0:
                title = response.css('.link4::text').get(),
                website = "www.gtstore.pk",
                price = response.css('span.price2>strong::text').get(),
                rating = "'None'",
                review = "'None'"
                clean_img = "'www.gtstore.pk'"
                writer.writerow(processing([title, website, price, rating, review, clean_img]))



'''
    def parse2(self, response):
        if (str(response.request.headers.get('referer'))).find("czone") >= 0:
            yield {
                'review' : response.css('span#producttabs1_rptReviews_ctl00_spnReviewSubject::text').extract(),
            }#add if conditions to make sure parse2 controls the flow of program
        elif (str(response.request.headers.get('referer'))).find("eezepc") >= 0:
            yield{
                'rating' : response.css('.rating::text').get(),
                'review' : response.css('div.wcpr-review-content-short::text').getall()
            }

'''
if __name__=="__main__":
    process = CrawlerProcess()
    process.crawl(ProductsSpider)
    process.start('example.csv')
    df = pd.read_csv("example.csv",names = ["Title","Website","Price","Rating","Reviews","Img_URLS"])
    df = df.sort_values(by= ["Price"])
    print(df[["Title","Price"]])







