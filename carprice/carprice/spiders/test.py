import scrapy


class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/',
    ]

    name = "quotes"

    def start_requests(self):
        headers = {
            'Content-type': 'application/json',
            'User-Agent':"My User Agent 1.0",
            'Accept': '*/*',
            "Postman-Token": "2400114c-e7fc-486d-ad32-b2aee2866452",
            'Host': 'api-gateway.driveway.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Length': '6439',
        }
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')