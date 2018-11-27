import scrapy
from scrapprj.items import Product
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class catalog(scrapy.spiders.CrawlSpider):
    name = 'catalog'
    allowed_domains = ['shop.vostok.ru']
    start_urls = ['https://shop.vostok.ru/catalog/'  # /sredstva-zaschity/',
                  # 'https://shop.vostok.ru/catalog/odezhda/',
                  # 'https://shop.vostok.ru/catalog/zaschita-ruk/',
                  # 'https://shop.vostok.ru/catalog/obuv/',
                  # 'https://shop.vostok.ru/catalog/drugoe/'
                  ]
    lastpage = 1
    rules = [Rule(LinkExtractor(allow=[
        r'https:\/\/shop\.vostok\.ru\/catalog\/((odezhda)|(drugoe)|(obuv)|(zaschita-ruk)|(sredstva-zaschity))\/(\?page=\d+)+'
    ]), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=[
            r'https:\/\/shop\.vostok\.ru\/catalog\/((odezhda)|(drugoe)|(obuv)|(zaschita-ruk)|(sredstva-zaschity))\/(\?page=\d+)*'
        ]), follow=True)
    ]

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     for item in response.xpath('//div[@class="pager js-pagination"]/a/@data-page'):
    #         num = int(item.extract())
    #         if(num > self.lastpage):
    #             self.lastpage = num
    #     pageurl = '?page='
    #     for pagenum in range(1, self.lastpage+1):
    #         yield response.follow(response.url+pageurl+str(pagenum), callback=self.parse_page)

    def parse_page(self, response):
        for item in response.xpath('//article[@class="catalog-product-item"]'):
            cur = Product()
            cur['name'] = item.xpath('./@data-title').extract()
            cur['index'] = item.xpath('./@data-catalog-cod').extract()
            cur['cat'] = item.xpath('./@data-first-category').extract()
            cur['price'] = item.xpath('./@data-price').extract()
            yield cur
