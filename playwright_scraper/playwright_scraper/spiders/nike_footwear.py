import scrapy


class NikeFootwearSpider(scrapy.Spider):
    name = "nike_footwear"
    allowed_domains = ["www.nike.com"]
    
    async def start(self):
        url = "https://www.nike.com/w/shoes-y7ok"
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_page_coroutines": [
                    # wait for the product cards to appear
                    ("wait_for_selector", "div.product-card__body")
                ]
            },
            callback=self.parse
        )

    def parse(self, response):
        # iterate over product cards
        for product in response.css("div.product-card__body"):
            # product name
            name = product.css("div.product-card__title::text").get()
            
            # subtitle (like category)
            subtitle = product.css("div.product-card__subtitle::text").get()
            
            # price
            price = product.css("div.product-price.is--current-price::text").get()
            
            # url (Nike sometimes uses the product-card__title div as a link role, or <a>. Try both.)
            url = product.css("a").attrib["href"]
            
            item = {
                "name": name,
                "subtitle": subtitle,
                "price": price,
                "url": url
            }
            print(item)
            yield item
