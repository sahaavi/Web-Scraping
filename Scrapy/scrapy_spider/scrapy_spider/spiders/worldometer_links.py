import scrapy


class WorldometerLinksSpider(scrapy.Spider):
    name = "worldometer_links"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        # Extracting  country names and links
        countries = response.xpath('//td/a') # Extracting "a" elements for each country
        
        # Looping through the countries list
        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get() # by this we'll get the relative link of each country
            # if we want to work with absolute link
            # we can do this by using concatenation or by using response.urljoin()

            # absolute_url = f"https://www.worldometers.info/{link}" # this is one way to do this
            # absolute_url = response.urljoin(link) # this is another way to do this

            # to check the absolute url
            # yield scrapy.Request(url=absolute_url) # if u see 200 in response then it's working fine

            # Return data extracted
            yield {
                "country_name": country_name, 
                "link": link
                }
            
            # to get the data from the relative url
            yield response.follow(url=link) # if u see 200 in response then it's working fine