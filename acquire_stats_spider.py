import scrapy

class RepoSpider(scrapy.Spider):
    name = "repos"

    def start_requests(self):
        start_urls = [
            'https://github.com/sorrycc/awesome-javascript'
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

        for title, link in dict.items():
            yield scrapy.Request(url=link, callback=self.parse)

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