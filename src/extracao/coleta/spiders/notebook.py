import scrapy


class NotebookSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook"]
    page_count = 1
    max_page = 10

    def parse(self, response):
        products = response.css('li.ui-search-layout__item')
        
        for product in products:
            
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            yield {
                'seller': product.css('span.poly-component__seller::text').get(),
                'name' : product.css('a.poly-component__title::text').get(),
                'reviews_rating': product.css('span.poly-reviews__rating::text').get(),
                'reviews_total': product.css('span.poly-reviews__total::text').get(),
                'old_money': prices[0] if len (prices) > 0 else None,
                'new_money': prices[1] if len (prices) > 1 else None
            }
            if self.page_count < self.max_page:
                self.page_count += 1
                offset = (self.page_count - 1) * 50 + 1
                next_page = f"https://lista.mercadolivre.com.br/notebook_Desde_{offset}"
                yield scrapy.Request(url=next_page, callback=self.parse)