import scrapy


class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"] # The root domain that the spider is allowed to crawl
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"] # This is the URL that the spider will start from

    def parse(self, response):
        # Extracting title and country names
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a/text()").getall()

        # Return data extracted
        yield {
            "title": title, 
            "countries": countries
            }