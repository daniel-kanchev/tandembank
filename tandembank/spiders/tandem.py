import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from tandembank.items import Article


class TandemSpider(scrapy.Spider):
    name = 'tandem'
    start_urls = ['https://www.tandem.co.uk/blog']

    def parse(self, response):
        links = response.xpath('//a[@class="cardchiplink"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

        next_page = response.xpath('//a[@class="w-pagination-next next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="heading-9"]/text()').get().strip()
        date = response.xpath('//div[@class="publishdate"]//text()').get().strip()
        date = datetime.strptime(date, '%B %d, %Y')
        date = date.strftime('%Y/%m/%d')
        content = response.xpath('//div[@class="articlecontent w-richtext"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()
        author = response.xpath('//div[@class="authorname"]//text()').get()
        category = response.xpath('//div[@class="articletags"]//text()').get()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('author', author)
        item.add_value('category', category)

        return item.load_item()

# response.xpath('').get()
