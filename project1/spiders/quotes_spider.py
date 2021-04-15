import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = f'quotes-{page}.html'
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log(f'Saved file {filename}')

    # allowed_domains = ['quotes.toscrape.com']
    # page = 1
    # start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    # def parse(self, response):
    #     data = json.loads(response.text)
    #     for quote in data["quotes"]:
    #         yield {"quote": quote["text"]}
    #     if data["has_next"]:
    #         self.page += 1
    #         url = f"http://quotes.toscrape.com/api/quotes?page={self.page}"
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tag::text').getall(),
    #         }

    #     next_page = response.css('li.next a::attr(href)').get()
    #     if next_page is not None:
    #         yield response.follow(next_page, callback=self.parse)

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }