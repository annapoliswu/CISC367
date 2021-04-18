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
            'description' : response.xpath('normalize-space(.//div[@class="productdescription"])').extract()[0],
            'price' : float(response.xpath("//div[@class='price']/text()").re(r'\d+.\d\d')[0]),
            'pagecount' : response.css('div.pagecount::text').get(),
            'publisher': response.css('div.publisher a::text').get(),
            'writer': response.css('div.writer a::text').get(),
            'artist': response.css('div.artist a::text').get(),
            'coverartist' : response.css('div.coverartist::text').get(),
            'productcode' : response.css('div.diamondcode::text').get(),
            'upc' : response.css('div.upc::text').get(),
            'color' : response.css('div.color::text').get(),
            'format' : response.css('div.format::text').get()
        }

    """
    Note, format after scraping. Cast on null or string cut on null, no yield output. Fill in when converting to CSV.

    """