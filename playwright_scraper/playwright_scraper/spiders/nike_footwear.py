import scrapy
from scrapy_playwright.page import PageMethod

# scrolling_script = """
# //scroll until page stops loading products
# () => {
#     return new Promise(resolve => {
#         let lastHeight = 0;
#         let attempts = 0;

#         function scrollStep() {
#             window.scrollTo(0, document.body.scrollHeight);
#             const currentHeight = document.body.scrollHeight;

#             if(currentHeight !== lastHeight){
#                 lastHeight = currentHeight;
#                 attempts = 0;
#             } else {
#                 attempts++;
#             }

#             // stop after 5 attempts with no new height increase
#             if(attempts >= 5){
#                 resolve();
#             } else {
#                 setTimeout(scrollStep, 500 + Math.random() * 500);
#             }
#         }
#         scrollStep();
#     });
# }
# # //scroll down the page 8 times
# # const scrolls = 8
# # let scrollCount = 0

# # //scroll down and then wait for random interval within .25 and 1 sec
# # const scrollInterval = setInterval(() => {
# #     window.scrollTo(0, document.body.scrollHeight)
# #     scrollCount++

# #     if(scrollCount == scrolls){
# #         clearInterval(scrollInterval)
# #     }
# # }, Math.random() * (1000 - 250) + 250)
# """

# class NikeFootwearSpider(scrapy.Spider):
#     name = "nike_footwear"
#     allowed_domains = ["www.nike.com"]
    
#     async def start(self):
#         url = "https://www.nike.com/w/shoes-y7ok"
#         yield scrapy.Request(url,meta={
#                 "playwright": True,
#                 "playwright_page_coroutines": [
#                     # wait for the product cards to appear
#                     ("wait_for_selector", "div.product-card__body"),
#                     PageMethod("evaluate", scrolling_script),
#                     PageMethod("wait_for_timeout", 10000)
#                 ]
#             },
#         callback=self.parse
#         )

#     def parse(self, response):
#         # iterate over product cards
#         for product in response.css("div.product-card__body"):
#             # product name
#             name = product.css("div.product-card__title::text").get()
            
#             # subtitle (like category)
#             subtitle = product.css("div.product-card__subtitle::text").get()
            
#             # price
#             price = product.css("div.product-price.is--current-price::text").get()
            
#             # url (Nike sometimes uses the product-card__title div as a link role, or <a>. Try both.)
#             url = product.css("a").attrib["href"]
            
#             item = {
#                 "name": name,
#                 "subtitle": subtitle,
#                 "price": price,
#                 "url": url
#             }
#             print(item)
#             yield item

#diff version that uses nike's feed api to scrape with JSON output

class NikeFootwearSpider(scrapy.Spider):
    name = "nike_footwear"
    allowed_domains = ["nike.com"]
    start_urls = ["https://www.nike.com/w/shoes-y7ok"]

    async def start(self):
        url = self.start_urls[0]
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.product-card__body"),
                    PageMethod(
                        "evaluate",
                        """
                        async () => {
                            let previousHeight = 0;
                            while (true) {
                                window.scrollBy(0, document.body.scrollHeight);
                                await new Promise(resolve => setTimeout(resolve, 3000));
                                let newHeight = document.body.scrollHeight;
                                if (newHeight === previousHeight) break;
                                previousHeight = newHeight;
                            }
                        }
                        """
                    )
                ],
            },
            callback=self.parse,
        )

    def parse(self, response):
        for product in response.css("div.product-card__body"):
            items= {
                "name": product.css("div.product-card__title::text").get(),
                "subtitle": product.css("div.product-card__subtitle::text").get(),
                "price": product.css("div.product-price.is--current-price::text").get(),
                "url": product.css("a::attr(href)").get(),
            }
            print(items)
            yield items