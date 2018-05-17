import scrapy

class RepoSpider(scrapy.Spider):
    name = "repos"

    def start_requests(self):
        start_urls = [
            'https://github.com/vsouza/awesome-ios'
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parseStartPages)

    def parseStartPages(self, response):
        self.parse(response)

    def parse(self, response):
        statTypes = ['watch', 'star', 'fork']
        dict = {}

        # Get url
        dict['url'] = response.request.url

        # Get name
        dict['name'] = response.css('.repohead-details-container .public [itemprop=name] a::text').extract_first()

        # Get statistics
        for stat in response.css('.pagehead-actions'):
            for index, type in enumerate(statTypes):
                strInType = stat.css('a.social-count::text')[index].extract()
                strInType = strInType.replace(" ", "")
                strInType = strInType.replace("\n", "")
                strInType = strInType.replace(",", "")
                dict[type] = int(strInType)
                
        yield dict

        # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)