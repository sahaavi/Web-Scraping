import scrapy
from scrapy import FormRequest

class QuotesLoginSpider(scrapy.Spider):
    name = "quotes_login"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    # Parsing the csrf_token, username and password
    def parse(self, response):
        csrf_token = response.xpath("//input[@name='csrf_token']/@value").get()
        # sending FormRequest (FormRequest extends the base Request with functionality for dealing with HTML forms)
        # FormRequest.from_response() simulates a user login
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf_token': csrf_token,
                'username': 'admin',
                'password': 'admin'
            },
            callback=self.after_login
        )
    # here we define the after_login function we used in callback
    def after_login(self, response):
        # If there's a "logout" text on the page, print "Successfully logged in!"
        if response.xpath("//a[@href='/logout']/text()").get():
            print('Successfully logged in!')
