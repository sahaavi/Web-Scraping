import scrapy
from scrapy_splash import SplashRequest

class AdamchoiParseSpider(scrapy.Spider):
    name = "adamchoi_parse"
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
        
    # As usual, we use the parse function to extract data with xpaths
    def parse(self, response):
        rows = response.xpath('//tr')

        for row in rows:
            date = row.xpath('./td[1]/text()').get()
            home_team = row.xpath('./td[2]/text()').get()
            score = row.xpath('./td[3]/text()').get()
            away_team = row.xpath('./td[4]/text()').get()
            yield {
                'date':date,
                'home_team':home_team,
                'score':score,
                'away_team':away_team,
            }