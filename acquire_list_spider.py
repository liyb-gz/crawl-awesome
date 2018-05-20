import scrapy

class RepoSpider(scrapy.Spider):
    name = "repos"

    def start_requests(self):
        start_urls = [
            'https://github.com/vsouza/awesome-ios'
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.findList)

    def findList(self, response):
        dict = {}
        # Get statistics
        for anchor in response.css('.markdown-body a'):
        # anchor = response.css('.markdown-body a')[0]
            link = anchor.css('a::attr(href)').extract_first()
            title = anchor.css('a::text').extract_first()

            if link.find('github.com') != -1 and link.find('.md') == -1:
                dict[title] = link

        yield dict