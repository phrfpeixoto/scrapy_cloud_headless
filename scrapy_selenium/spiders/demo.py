import scrapy
from selenium import webdriver
from selenium.webdriver import FirefoxProfile

from scrapy_selenium.settings import CRAWLERA_HEADLESS_PROXY, CRAWLERA_HEADLESS_PORT


class DemoSpider(scrapy.Spider):
    name = 'demo'
    start_urls = ['https://quotes.toscrape.com/js']

    def __init__(self, *args, **kwargs):
        super(DemoSpider, self).__init__(*args, **kwargs)

        profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", CRAWLERA_HEADLESS_PROXY)
        profile.set_preference("network.proxy.http_port", CRAWLERA_HEADLESS_PORT)
        profile.set_preference("network.proxy.ssl", CRAWLERA_HEADLESS_PROXY)
        profile.set_preference("network.proxy.ssl_port", CRAWLERA_HEADLESS_PORT)
        profile.accept_untrusted_certs = True

        options = webdriver.FirefoxOptions()
        options.add_argument("--window-size 1920,1080")
        options.add_argument("--headless")
        # Required to run the browser inside the docker (as root)
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Firefox(options=options, firefox_profile=profile)

    def parse(self, response, **kwargs):
        """
        Note: This is a trivial example to prove Selenium can be integrated with Crawlera and
        executed within Scrapy Cloud. I DO NOT RECOMMEND that you use a selenium driver to
        issue requests from within your spider's parse method.
        """

        quotes = response.css("div.quote")
        assert len(quotes) == 0

        self.driver.get(response.url)
        quotes = self.driver.find_elements_by_css_selector('div.quote')
        assert len(quotes) > 0
        for quote in quotes:
            yield {
                'quote': quote.find_element_by_css_selector('span').text,
                'author': quote.find_element_by_css_selector('small').text,
            }
        next_page_url = response.css('nav li.next a ::attr(href)').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))
