import scrapy
from selenium import webdriver
from selenium.webdriver import FirefoxProfile

from scrapy_selenium.settings import CRAWLERA_HEADLESS_PROXY, CRAWLERA_HEADLESS_PORT


class DemoSpider(scrapy.Spider):
    name = 'demo'
    start_urls = ['http://quotes.toscrape.com/js']

    def __init__(self, *args, **kwargs):
        super(DemoSpider, self).__init__(*args, **kwargs)

        profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", CRAWLERA_HEADLESS_PROXY)
        profile.set_preference("network.proxy.http_port", CRAWLERA_HEADLESS_PORT)
        profile.set_preference("network.proxy.ssl", CRAWLERA_HEADLESS_PROXY)
        profile.set_preference("network.proxy.ssl_port", CRAWLERA_HEADLESS_PORT)

        options = webdriver.FirefoxOptions()
        options.add_argument("--window-size 1920,1080")
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options, firefox_profile=profile)

    def parse(self, response):
        self.driver.get(response.url)
        for quote in self.driver.find_elements_by_css_selector('div.quote'):
            yield {
                'quote': quote.find_element_by_css_selector('span').text,
                'author': quote.find_element_by_css_selector('small').text,
            }
        next_page_url = response.css('nav li.next a ::attr(href)').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))
