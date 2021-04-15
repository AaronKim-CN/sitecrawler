import scrapy
from scrapy_selenium import SeleniumRequest

class PalSpider(scrapy.Spider):
    name = 'pal'
    allowed_domains = ['https://www.palcloset.jp/']

    #Setting
    endpage = 1
    original_url = 'https://www.palcloset.jp/display/display/?b=&c=18&type=01&p='
    #####

    urls = []

    for p in range(endpage):
        urls.append(original_url+str(p+1))

    start_urls = urls

    def parse(self, response):

        itemlist = response.xpath('//*[@id="item_list"]')
        for img in itemlist.css('ul').css('li'): 
            # print(img.css('img').attrib['src']) 
            # print(img.css('div.textOverflow p::text').get())
            im_url = img.css('img').attrib['src']
            title = img.css('div.textOverflow p::text').get()
            im_id = im_url.split("/")[-1]

            yield {
                'im_id': im_id,
                'im_url': im_url,
                'title': title
            }