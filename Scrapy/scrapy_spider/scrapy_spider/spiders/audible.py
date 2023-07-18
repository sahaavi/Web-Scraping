import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.ca"]
    start_urls = ["https://www.audible.ca/search"]

    def parse(self, response):
        # Getting the box that contains all the info we want (title, author, length)
        container = response.xpath('//div[@class="adbl-impression-container "]')

        products = container.xpath('.//li[contains(@class, "productListItem")]')

        # Looping through each product listed in the products box
        for product in products:
            book_title = product.xpath('.//h3[contains(@class, "bc-heading")]/a/text()').get()
            book_author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()
            book_narrator = product.xpath('.//li[contains(@class, "narratorLabel")]/span/a/text()').getall()
            runtimeLabel = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()
            book_length = runtimeLabel.strip().replace("\n", "").replace('Length:', '').strip()
            releaseDateLabel = product.xpath('.//li[contains(@class, "releaseDateLabel")]/span/text()').get()
            release_date = releaseDateLabel.strip().replace(" ", "").replace("\n", "").replace('Releasedate:', '')
            languageLabel = product.xpath('.//li[contains(@class, "languageLabel")]/span/text()').get()
            language = languageLabel.strip().replace(" ", "").replace("\n", "").replace('Language:', '') 
            regular_price = product.xpath('.//p[contains(@class, "buybox-regular-price")]/span[2]/text()').get()
            regular_price = regular_price.strip().replace(" ", "").replace("\n", "").replace('$', '')

            # Return data extracted
            yield {
                'title': book_title,
                'author': book_author,
                'narrator': book_narrator,
                'length': book_length,
                'release_date': release_date,
                'language': language,
                'regular_price': regular_price
            }