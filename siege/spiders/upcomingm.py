import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class UpcomingmSpider(CrawlSpider):
    name = 'upcomingm'
    allowed_domains = ['siege.gg']

    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='http://siege.gg/matches', headers={
        'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@id='upcoming']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
    )

    def set_user_agent(self, request):
        request.headers['User-Agent']=self.user_agent
        return request

    def parse_item(self, response):
        team1 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text())").get() #team 1 data left side
        team2 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text()[2])").get() #team2 data rigt side
        result_1 = response.xpath("normalize-space((//div[@class='match__overview-lower'])[1]/div/text())").get() #left 
        result_2 = response.xpath("normalize-space((//div[@class='match__overview-lower'])[2]/div/text())").get() #right

        yield{
            'title': team1 + ' vs ' +  team2,
            'competation' : response.xpath("normalize-space(//span[@class='meta__item meta__competition']/a/text())").get(),
            'result': result_1 + ' ' + result_2,
            'time' : response.xpath("normalize-space(//div[@class='entry__meta']/time/text())").get(),
            'country' : response.xpath("normalize-space(//span[@class='mr-1']/text())").get(),
            'roster' : {
                team1 : response.xpath("//div[@class='col-12 col-md match__roster team--a']//h5/text()").getall(),
                team2 : response.xpath("//div[@class='col-12 col-md match__roster team--b']//h5/text()").getall()
            }
        }
