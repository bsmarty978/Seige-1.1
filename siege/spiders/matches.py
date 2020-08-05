import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MatchesSpider(CrawlSpider):
    name = 'matches'
    allowed_domains = ['siege.gg']

    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://siege.gg/matches?tab=results', headers={
        'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@id='results']/a"), callback='parse_item', follow=True, process_request='set_user_agent'), #for every match
        Rule(LinkExtractor(restrict_xpaths="//a[@rel='next']"), process_request='set_user_agent'),    #for next page
    )

    def set_user_agent(self, request):
        request.headers['User-Agent']=self.user_agent
        return request

    def parse_item(self, response):
        team1 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text())").get() #team 1 data left side
        team2 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text()[2])").get() #team2 data rigt side

        result_1 = response.xpath("normalize-space((//div[@class='match__overview-lower'])[1]/div/text())").get() #left 
        result_2 = response.xpath("normalize-space((//div[@class='match__overview-lower'])[2]/div/text())").get() #right

        #stats_cond = response.xpath("normalize-space(//div[@class='alert alert-default small']/text())").get()
        #(//h2[@class = 'mb-0']/following-sibling::node())[2] --  player stats emtpy direct 
        stats_cond = response.xpath("normalize-space(//div[@class='row row--padded match__player-stats']/div/div/text())").get() # this condition checks in player stasts table for No player stats data string
        stat_dict = {}   #empty string to store every player stats
        if stats_cond != 'No player stats data available.':  #loop to intrate through every player make dict of each
            for player in response.xpath("//table[@class = 'table table-sm table-hover table--stats table--player-stats js-dt--player-stats js-heatmap  w-100']//tbody/tr"):
                player_name = player.xpath("normalize-space((.//td[@class = 'team--a sp__player js-heatmap-ignore']/text())[position() mod 2 != 1 and position() > 1])").get() 
                dic = {
                    'name' : player_name,
                    'rating': player.xpath("normalize-space(.//td[@class = 'sp__rating js-heatmap-td font-weight-bold']/text())").get(),
                    'kd': player.xpath("normalize-space(.//td[@class='sp__kills text-nowrap']/text())").get(),
                    'entry': player.xpath("normalize-space(.//td[@class='sp__ok text-nowrap']/text())").get(),
                    'kost': player.xpath("normalize-space(.//td[@class='sp__kost js-heatmap-td']/text())").get(),
                    'kpr': player.xpath("normalize-space(.//td[@class='sp__kpr js-heatmap-td']/text())").get(),
                    'srv': player.xpath("normalize-space(.//td[@class='sp__srv js-heatmap-td']/text())").get(),
                    '1vx': player.xpath("normalize-space(.//td[@class='sp__1vx']/text())").get(),
                    'plant': player.xpath("normalize-space(.//td[@class='sp__plant']/text())").get(),
                    'hs': player.xpath("normalize-space(.//td[@class='sp__hs']/text())").get(),
                }
                stat_dict.update({player_name:dic})
        else: #if no stats data available
            stat_dict = stats_cond

        #match meta data and stats combined
        yield{
            'title': team1 + ' vs ' +  team2,
            'title_result': team1 + ' ' + result_1 + ' vs ' + result_2 + ' ' + team2,
            'result': result_1 + ' ' + result_2,
            'competation' : response.xpath("normalize-space(//span[@class='meta__item meta__competition']/a/text())").get(),
            'time' : response.xpath("normalize-space(//div[@class='entry__meta']/time/text())").get(),
            'country' : response.xpath("normalize-space(//span[@class='mr-1']/text())").get(),
            'roster' : {
                team1 : response.xpath("//div[@class='col-12 col-md match__roster team--a']//h5/text()").getall(),
                  team2 : response.xpath("//div[@class='col-12 col-md match__roster team--b']//h5/text()").getall()
            },
            'stats': stat_dict
        }

