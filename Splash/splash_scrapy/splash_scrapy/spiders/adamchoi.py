import scrapy
from scrapy_splash import SplashRequest

class AdamchoiSpider(scrapy.Spider):
    name = "adamchoi"
    allowed_domains = ["www.adamchoi.co.uk"]
    # start_urls = ["https://www.adamchoi.co.uk/overs/detailed"]

    script = """
        function main(splash, args)
            -- If a website doesn't render correctly, disabling Private mode might help
            splash.private_mode_enabled = false
            -- Go to the URL set on the splash browser and then wait 3 seconds to let the page render
            assert(splash:go(args.url))
            assert(splash:wait(3))
            -- Select all the elements that have the css selector "label.btn.btn-sm.btn-primary"
            all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
            -- Two elements were selected. We want to click on the second button, then wait 3 seconds to let the page render
            all_matches[2]: mouse_click()
            assert (splash:wait(3))
            -- Increase the viewport to make all the content visible
            splash: set_viewport_full()
            return {splash: png(), splash: html()}
        end
"""

    # Define a start_requests function to connect scrapy and splash
    def start_requests(self):
        yield SplashRequest(url='https://www.adamchoi.co.uk/overs/detailed', callback=self.parse,
                            endpoint='execute', args={'lua_source':self.script})

    # Let's verify if the connection splash-scrapy is working getting the html
    def parse(self, response):
        print(response.body)
