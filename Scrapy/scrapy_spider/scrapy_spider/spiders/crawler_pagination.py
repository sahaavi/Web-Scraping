import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time


class CrawlerPaginationSpider(CrawlSpider):
    name = "crawler_pagination"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies_letter-X"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='scripts-list']/a")), callback="parse_item", follow=True), 
        Rule(LinkExtractor(restrict_xpaths=("//a[@rel='next']"))) # this is the pagination rule (next page)
        # we are not using callback in the 2nd rule because we are getting the data of each page in the first rule using callback
        # we are not using follow=True in the 2nd rule because we are not using callback in the 2nd rule
        )
    # LinkExtractor funciton will automatically extract all the links thats why we dont need to use @href

    def parse_item(self, response):
        # Getting the article box that contains the data we want (title, plot, etc)
        article = response.xpath("//article[@class='main-article']")

        # Extract the data we want and then yield it
        yield {
            'title': article.xpath("./h1/text()").get(),
            # avoid these to make crawling faster
            # 'plot': article.xpath("./p/text()").get(),
            # 'transcript': article.xpath("./div[@class='full-script']/text()").getall(),
            'url': response.url,
        }

    # This will give error message: 429 Unknown Status
            
# The error message you encountered, "429 Unknown Status," indicates that the server is returning a status code 429, 
# which typically means "Too Many Requests." This happens when you make too many requests to the server within a short period of time, 
# and the server is rate-limiting your access to prevent abuse.

# To fix this issue, you need to implement proper rate-limiting in your Scrapy spider to avoid overwhelming 
# the server with too many requests. You can do this by setting a download delay in your spider to slow down the rate of requests.

# goto settings.py and search for DOWNLOAD_DELAY valriable and uncomment it and set it to 0.5
# if you can't find this variable in settings, then add it manually
# DOWNLOAD_DELAY = 0.5