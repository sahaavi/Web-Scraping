import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsCrawlerSpider(CrawlSpider):
    name = "transcripts_crawler"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies"]
    
    rules = (Rule(LinkExtractor(restrict_xpaths="//ul[@class='scripts-list']/a"), callback="parse_item", follow=True),)
    # LinkExtractor funciton will automatically extract all the links thats why we dont need to use @href

    def parse_item(self, response):
        # to check if we getting the movie links
        # print(response.url)

        # Getting the article box that contains the data we want (title, plot, etc)
        article = response.xpath("//article[@class='main-article']")

        # Extract the data we want and then yield it
        yield {
            'title': article.xpath("./h1/text()").get(),
            'plot': article.xpath("./p/text()").get(),
            'transcript': article.xpath("./div[@class='full-script']/text()").getall(),
            'url': response.url,
        }
