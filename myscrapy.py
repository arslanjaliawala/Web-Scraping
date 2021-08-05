import scrapy
class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = ['https://linnasmartlimited.com/product-category/homeware-appliances/',
                  'https://linnasmartlimited.com/product-category/kitchenware/',
                  'https://linnasmartlimited.com/product-category/sports-equipments/']
    def parse(self,response):
        clean_image_urls = []
        for product in response.css('div.astra-shop-summary-wrap'):
            prices = product.css('span.woocommerce-Price-amount.amount>bdi::text').getall()
            yield{
                'category': product.css('span.ast-woo-product-category::text').get().strip(),
                'title': product.css('.woocommerce-loop-product__title::text').get(),
                'oprice' : prices[0],
                'dprice' :
                            prices[0] if len(prices) == 1
                            else prices[1]
            }
        raw_image_urls = response.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link img::attr(src)').getall()
        for img_url in raw_image_urls:
            clean_image_urls.append(response.urljoin(img_url))
        yield{
            'image_urls' : clean_image_urls
        }


