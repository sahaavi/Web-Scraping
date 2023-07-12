# Web-Scraping

## BeautifulSoup
BeautifulSoup can pull data out of HTML in XML files. This library is best choice for beginners beacuse it is the easiest web scrapping library in Python.  
Unfortunately, beautifulsoup doesn't have the support for JavaScript driven websites. This is a big disadvantage as nowadays majority of the websites run on JavaScript. Also beautifulsoup is inefficient and it has some dependencies that make it complicated to transfer a code between projects.

## Selenium
Selenium wasn't actually designed for web scrapping. In fact, selenium is Web driver designed to render Web pages for test automation of Web applications. This makes selenium great for web scraping because many websites rely on JavaScript to create dynamic content on the page.  
So we can say that selenium is one of the best libraries for scraping JavaScript driven websites. Another advantage of selenium is that is easier to learn than the Scrapy.  
Unfortunately, selenium is a slow. Web Scraping with selenium is a slower than HTP request to the web browser because all the scripts present
on the Web page will be executed.  
However, if it isn't our top priority, selenium will be a good option.

## Scrapy
Scrapy is a web scraping framework built especially for web scraping and written entirely in Python. This is without a doubt the most complete web scraping tool in Python.  
Unfortunately, a scrapie is harder to learn than selenium or beautifulsoup.  
That said, one of the biggest advantages of a scrapie is the speed, since it's synchronous scrapy spiders don't have to wait to make requests one at a time, but it can make requests in parallel. This increases efficiency, which makes it memory and CPU efficient compared to the beautifulsoup and selenium. You can easily store data in databases, create crullers and do more with scrapy.

## So which one is the best?
- BeautifulSoup will be great for beginners.
- Selenium will be good for small projects that need to scrape JavaScript driven websites.
- Scrapy will be great for large projects where speed is priority.