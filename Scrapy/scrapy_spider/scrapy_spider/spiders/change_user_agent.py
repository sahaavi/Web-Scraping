import scrapy


class ChangeUserAgentSpider(scrapy.Spider):
    name = "change_user_agent"
    allowed_domains = ["www.audible.ca"]
    # start_urls = ["https://www.audible.ca/search"] # This is not needed anymore since we are using scrapy_requests() method

    # Changing the user agent so that the website doesn't block us or couldn't identify us as a bot/scraping tool
    def start_requests(self):
        yield scrapy.Request(url="https://www.audible.ca/search", callback=self.parse, 
                       headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'}
                       )

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
                'regular_price': regular_price,
                'User-Agent':response.request.headers['User-Agent']
            }

            # Getting the pagination bar (pagination) and then the link within the next page button (next_page_url)
            pagination = response.xpath('//ul[contains(@class , "pagingElements")]')
            next_page_url = pagination.xpath('.//span[contains(@class , "nextButton")]/a/@href').get()

            # Going to the "next_page_url" link
            if next_page_url:
                yield response.follow(url=next_page_url, callback=self.parse,
                                      headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'}
                                      )

