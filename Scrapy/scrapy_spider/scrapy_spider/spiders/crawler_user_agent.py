import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlerUserAgentSpider(CrawlSpider):
    name = "crawler_user_agent"
    allowed_domains = ["subslikescript.com"]
    # start_urls = ["https://subslikescript.com/movies_letter-X"]

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'

    # Editing the user-agent in the request sent
    def start_requests(self):
        yield scrapy.Request(url='https://subslikescript.com/movies_letter-X', headers={
            'user-agent':self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='scripts-list']/a")), callback="parse_item", follow=True, process_request='set_user_agent'), 
        Rule(LinkExtractor(restrict_xpaths=("//a[@rel='next']")), process_request='set_user_agent')
        )
    # LinkExtractor funciton will automatically extract all the links thats why we dont need to use @href

    # Setting the user-agent
    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

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
            'user-agent': response.request.headers['User-Agent'],
        }

