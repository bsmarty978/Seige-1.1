import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.crawler import CrawlerProcess
import pycountry as pc
class UpcomingmSpider(CrawlSpider):
    name = 'upcomingm'
    allowed_domains = ['siege.gg']

    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='http://siege.gg/matches', headers={
        'User-Agent': self.user_agent
        })

    rules = (
        # Rule(LinkExtractor(restrict_xpaths="//div[@id='upcoming']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//div[@id='upcoming']/a"), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths="//a[@rel='next']")),
    )

    def set_user_agent(self, request):
        request.headers['User-Agent']=self.user_agent
        return request

    def parse_item(self, response):
        team1 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text())").get() #team 1 data left side
        team2 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text()[2])").get() #team2 data rigt side
        # team1_flag = response.xpath("(//div[@class='match__overview-lower rounded overflow-hidden']//img)[1]/@src").get()
        # team2_flag = response.xpath("(//div[@class='match__overview-lower rounded overflow-hidden']//img)[2]/@src").get()
        team1_flag = response.xpath("(//div[@class='match__overview-lower rounded overflow-hidden'])[1]//img/@src").get()
        team2_flag = response.xpath("(//div[@class='match__overview-lower rounded overflow-hidden'])[2]//img/@src").get()
        result_1 = response.xpath("normalize-space((//div[@class='match__overview-lower'])[1]/div/text())").get() #left 
        result_2 = response.xpath("normalize-space((//div[@class='match__overview-lower'])[2]/div/text())").get() #right
        photos = {}
        #for getting photo links maing new loops for each teams roster
        # roster_a = response.xpath("//div[@class='col-12 col-md match__roster team--a']")
        # roster_b = response.xpath("//div[@class='col-12 col-md match__roster team--b']")

        player_details = []
        players_roster = response.xpath("//div[@class='roster__player']")

        for player in players_roster:
            ign = player.xpath("normalize-space(.//h5/text())").get()
            name = player.xpath("normalize-space(.//small/text()[position() mod 2 != 1 and position() > 1])").get()
            photo = player.xpath(".//img[@class='player__photo__img img-fluid']/@src").get()
            country = player.xpath("(.//img)[2]/@title").get()
            player_details.append({'ign':ign,'name':name,'photo':photo,'country':country})

        #For Teams Countries
        team_a_c = response.xpath("(//span[@class='match__flag mx-2'])[1]/img/@title").get().split(' ')[0]
        team_b_c = response.xpath("(//span[@class='match__flag mx-2'])[2]/img/@title").get().split(' ')[0]
        try:
            country_a = pc.countries.get(alpha_2= team_a_c).name
            country_b = pc.countries.get(alpha_2= team_b_c).name
        except:
            country_a = team_a_c
            country_b = team_b_c

        yield{
            'title': team1 + ' vs ' +  team2,
            'url' : response.url,
            'match_id' : int(response.url.split('/')[-1].split('-')[0]),
            'team_a': {'name':team1,'country':country_a,'flag':team1_flag},
            'team_b': {'name':team2,'country':country_b,'flag':team2_flag},
            # 'country': {'team_a':country_a,'team_b':country_b},
            # 'team_a_flag': team1_flag,
            # 'team_b_flag': team2_flag,
            'game' : "Rainbow Six Siege",
            'competation' : response.xpath("normalize-space(//span[@class='meta__item meta__competition']/a/text())").get(),
            'result': result_1 + ' ' + result_2,
            'time' : response.xpath("//div[@class='entry__meta']/time/@datetime").get(),
            'location' : response.xpath("normalize-space(//span[@class='meta__item match__location']/text())").get(),
            'roster' : {
                'team_a' : response.xpath("//div[@class='col-12 col-md match__roster team--a']//h5/text()").getall(),
                'team_b' : response.xpath("//div[@class='col-12 col-md match__roster team--b']//h5/text()").getall()
            },
            'player_details' : player_details
        }


# to run spider wihtin script
# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(UpcomingmSpider)
#     process.start()
    


# using sys method to directly run cmdline
# import sys
# from scrapy.cmdline import execute


# def gen_argv(s):
#     sys.argv = s.split()


# if __name__ == '__main__':
#     gen_argv('scrapy crawl abc_spider')
#     execute()