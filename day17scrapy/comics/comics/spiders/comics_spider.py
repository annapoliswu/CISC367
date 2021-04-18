import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "comics"
    start_urls = [
        'https://www.instocktrades.com/publishers/dc'
    ]

    def parse(self, response):
        for item in response.css('div.item'):
            item_link = item.css('div.title a::attr(href)').get()
            if item_link is not None:
                item_link = response.urljoin(item_link)
                yield scrapy.Request(item_link, callback= self.parse_follow)

        next_page = response.css('a.btn.hotaction::attr(href)').getall()[-1]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_follow(self, response):
        yield{
            'title' : response.css('h1::text').get(),
            'description' : response.xpath('normalize-space(.//div[@class="productdescription"])').extract_first(default=''),
            'price' : float(response.xpath("//div[@class='price']/text()").re(r'\d+.\d\d')[0]),
            'pagecount' : response.xpath("//div[@class='pagecount']/text()").extract_first(default='').strip(),
            'publisher': response.css('div.publisher a::text').get(),
            'writer': response.xpath("//div[@class='writer']/a/text()").extract_first(default='').strip().title(),
            'artist': response.xpath("//div[@class='artist']/a/text()").extract_first(default='').strip().title(),
            'coverartist' : response.xpath("//div[@class='coverartist']/text()").extract_first(default='').strip().title(),
            'productcode' : response.xpath("//div[@class='diamondcode']/text()").extract_first(default='').strip(),
            'upc' : response.xpath("//div[@class='upc']/text()").extract_first(default='').strip(),
            'color' : response.xpath("//div[@class='color']/text()").extract_first(default='').strip().title(),
            'format' : response.xpath("//div[@class='format']/text()").extract_first(default='').strip().title(),
        }

    """
    Note, format after scraping. Cast on null or string cut on null, no yield output. Fill in when converting to CSV?

    """