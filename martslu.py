import scrapy
class ProductsSpider(scrapy.Spider):
    name = "martslu"
    start_urls = ['https://martslu.com/product-category/supplements/',
                  'https://martslu.com/product-category/homeware-appliances/',
                  'https://martslu.com/product-category/kitchenware/',
                  'https://martslu.com/product-category/pet-supplies/',
                  'https://martslu.com/product-category/sports-equipments/']


    def parse(self, response):
        for product in response.css('div.box-text.box-text-products'):
            prices = product.css('span.woocommerce-Price-amount.amount>bdi::text').getall()
            yield {
                'category': product.css('div.title-wrapper > p.category::text').get().strip(),
                'title': product.css('div.title-wrapper > p.name.product-title > a::text').get(),
                'oprice' : prices[0],
                'dprice' : prices[0] if len(prices) == 1
                else prices[1]
            }
