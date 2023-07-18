import scrapy


class WorldometerMultiLinksSpider(scrapy.Spider):
    name = "worldometer_multi_links"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        # Extracting  country names and links
        countries = response.xpath('//td/a') # Extracting "a" elements for each country
        
        # Looping through the countries list
        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get() # by this we'll get the relative link of each country
            
            # to get the data from the relative url
            yield response.follow(url=link, callback=self.parse_country, meta={'country':country_name}) # if u see 200 in response then it's working fine

    def parse_country(self, response):
        # Getting country names and each row element inside the population table
        country = response.request.meta['country']
        # both xpath are same
        # rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        rows = response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            # Return data extracted
            yield {
                'country': country,
                'year': year,
                'population': population
            }