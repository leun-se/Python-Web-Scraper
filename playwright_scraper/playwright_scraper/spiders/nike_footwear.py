import scrapy
from scrapy_playwright.page import PageMethod
from playwright_scraper.items import PlaywrightScraperItem
# USD to EUR
js_script = """
document.querySelectorAll(".product-card_body.div.product-price)
.forEach(e=>e.innerHTML=e.replace("$". "€"))
"""
class NikeFootwearSpider(scrapy.Spider):
    name = "nike_footwear"
    allowed_domains = ["nike.com"]
    start_urls = ["https://www.nike.com/w/shoes-y7ok"]

    async def start(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    # Wait for the first product
                    PageMethod("wait_for_selector", "div.product-card__body"),
                    # Scroll until no new products appear
                    PageMethod(
                        "evaluate",
                        """
                        async () => {
                            let lastHeight = 0;
                            while(true){
                                window.scrollBy(0, document.body.scrollHeight);
                                await new Promise(r => setTimeout(r, 1500));
                                let newHeight = document.body.scrollHeight;
                                if(newHeight === lastHeight) break;
                                lastHeight = newHeight;
                            }
                        }
                        """
                    ),
                    #PageMethod("evaluate", js_script),
                    PageMethod("wait_for_timeout", 2000)
                ],
            },
            callback=self.parse
        )

    def parse(self, response):
        """
    @url https://www.nike.com/w/shoes-y7ok
    @returns items 24 24
    @returns request 0 1
    @scrapes url name subtitle price 
        """
        for product in response.css("div.product-card__body"):
            item = PlaywrightScraperItem()
            item["name"] = product.css("div.product-card__title::text").get()
            item["subtitle"] = product.css("div.product-card__subtitle::text").get()
            item["price"] = product.css("div.product-price.is--current-price::text").get()
            item["url"] = product.css("a::attr(href)").get()
            yield item
        
        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(
                f"Navigating to next page with URL {next_page_url}."
            )
            yield scrapy.Request(
                url=next_page_url, 
                callback=self.parse,
                errback=self.log_error,
            )
            
    def log_error(self, failure):
        self.logger.error(repr(failure))