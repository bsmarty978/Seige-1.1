import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import HtmlResponse
import pycountry as pc
from scrapy.exceptions import CloseSpider

class MatchesSpider(CrawlSpider):
    name = 'matches'
    allowed_domains = ['siege.gg']

    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'

    def start_requests(self):
        # yield scrapy.Request(url='https://siege.gg/matches?tab=results')
        yield scrapy.Request(url='https://siege.gg/matches?tab=results', headers={
        'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@id='results']/a"), callback='parse_item', follow=True), #for every match
        Rule(LinkExtractor(restrict_xpaths="//a[@rel='next']")),    #for next page
    )

    def set_user_agent(self, request):
        request.headers['User-Agent']=self.user_agent
        return request

    def parse_item(self, response):
        team1 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text())").get() #team 1 data left side
        team2 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text()[2])").get() #team2 data rigt side
        # team1_flag = response.xpath("(//div[@class='match__overview-lower']//img)[1]/@src").get()
        # team2_flag = response.xpath("(//div[@class='match__overview-lower']//img)[2]/@src").get()
        team1_flag = response.xpath("(//div[@class='match__overview-lower rounded overflow-hidden'])[1]//img/@src").get()
        team2_flag = response.xpath("(//div[@class='match__overview-lower rounded overflow-hidden'])[2]//img/@src").get()
        # result_1 = response.xpath("normalize-space((//div[@class='match__overview-lower'])[1]/div/text())").get() #left 
        # result_2 = response.xpath("normalize-space((//div[@class='match__overview-lower'])[2]/div/text())").get() #right
        result_1 = response.xpath("normalize-space((//div[@class='match__overview-lower rounded overflow-hidden']//div)[1]//text())").get() #left 
        result_2 = response.xpath("normalize-space((//div[@class='match__overview-lower rounded overflow-hidden']//div)[2]//text())").get() #right
        
        #stats_cond = response.xpath("normalize-space(//div[@class='alert alert-default small']/text())").get()
        #(//h2[@class = 'mb-0']/following-sibling::node())[2] --  player stats emtpy direct 

        stats_cond = response.xpath("normalize-space(//div[@class='row row--padded match__player-stats']/div/div/text())").get() # this condition checks in player stasts table for No player stats data string
        # stats_cond = response.xpath("normalize-space(//div[@class='row row--padded match__player-stats']//div[@class='alert alert-secondary small']/text())").get() # this condition checks in player stasts table for No player stats data string
        stat_dict = {}
        stat_list = []   #empty string to store every player stats
        if stats_cond != 'No player stats data available.':  #loop to intrate through every player make dict of each
            
            #NOTE: After updates on DATE:(31-May-2021) player stats table is no longer avaible directly from.
                # For that i have made lazy patch that should work for now.

            #*This 2 objects are only used when player stats table in in Scrpit.  
            # script_obj = response.xpath("//script")[0].get().split("`")[1]
            # script_resp = HtmlResponse(url="fuck it",body = script_obj,encoding='utf-8')
             
            #NOTE: This are some loops that might work  if Base site changes.
            # for player in response.xpath("//table[@class = 'table table-sm table-hover table--stats table--player-stats js-dt--player-stats js-heatmap  w-100']//tbody/tr"):
            for player in response.xpath("//table[@class = 'table table-sm table-hover table--stats table--player-stats js-dt--player-stats js-heatmap w-100']//tbody/tr"):
            # for player in script_resp.xpath("//table//tbody/tr"):
                #NOTE: This Object where using HardCode class names which is changed to positions.
                # player_name = player.xpath("normalize-space((.//td[@class = 'team--a sp__player js-heatmap-ignore']/text())[position() mod 2 != 1 and position() > 1])").get() 
                # dic = {
                #     'name' : player_name,
                #     'rating': player.xpath("normalize-space(.//td[@class = 'sp__rating js-heatmap-td font-weight-bold']/text())").get(),
                #     'kd': player.xpath("normalize-space(.//td[@class='sp__kills text-nowrap']/text())").get(),
                #     'entry': player.xpath("normalize-space(.//td[@class='sp__ok text-nowrap']/text())").get(),
                #     'kost': player.xpath("normalize-space(.//td[@class='sp__kost js-heatmap-td']/text())").get(),
                #     'kpr': player.xpath("normalize-space(.//td[@class='sp__kpr js-heatmap-td']/text())").get(),
                #     'srv': player.xpath("normalize-space(.//td[@class='sp__srv js-heatmap-td']/text())").get(),
                #     '1vx': player.xpath("normalize-space(.//td[@class='sp__1vx']/text())").get(),
                #     'plant': player.xpath("normalize-space(.//td[@class='sp__plant']/text())").get(),
                #     'hs': player.xpath("normalize-space(.//td[@class='sp__hs']/text())").get(),
                # }
                player_name = player.xpath('normalize-space((.//td[1]/text())[position() mod 2 != 1 and position() > 1])').get() 
                dic = {
                    'name' : player_name,
                    'rating': player.xpath('normalize-space(.//td[2]/text())').get(),
                    'kd': player.xpath('normalize-space(.//td[3]/text())').get(),
                    'entry': player.xpath('normalize-space(.//td[4]/text())').get(),
                    'kost': player.xpath('normalize-space(.//td[5]/text())').get(),
                    'kpr': player.xpath('normalize-space(.//td[6]/text())').get(),
                    'srv': player.xpath('normalize-space(.//td[7]/text())').get(),
                    '1vx': player.xpath('normalize-space(.//td[8]/text())').get(),
                    'plant': player.xpath('normalize-space(.//td[9]/text())').get(),
                    'hs': player.xpath('normalize-space(.//td[10]/text())').get(),
                }
                #stat_dict.update({player_name:dic}) # it stores stats as key value dict like player name : stats
                stat_list.append(dic)                #this approch it make a list of players stats dict
        else: #if no stats data available
            stat_dict = stats_cond

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


        #match meta data and stats combined
        yield{
            'title': team1 + ' vs ' +  team2,
            'url' : response.url,
            'match_id' : int(response.url.split('/')[-1].split('-')[0]),
            'title_result': team1 + ' ' + result_1 + ' vs ' + result_2 + ' ' + team2,
            'team_a': {'name':team1,'country':country_a,'flag':team1_flag},
            'team_b': {'name':team2,'country':country_b,'flag':team2_flag},
            'game' : "Rainbow Six Siege",
            'result_a':result_1,
            'result_b':result_2,
            'result': result_1 + ' ' + result_2,
            'competation' : response.xpath("normalize-space(//span[@class='meta__item meta__competition']/a/text())").get(),
            'time' : response.xpath("//div[@class='entry__meta']/time/@datetime").get(),
            'location' : response.xpath("normalize-space(//span[@class='meta__item match__location']/text())").get(),
            'roster' : {
                'team_a' : response.xpath("//div[@class='col-12 col-md match__roster team--a']//h5/text()").getall(),
                'team_b' : response.xpath("//div[@class='col-12 col-md match__roster team--b']//h5/text()").getall()
            },
            'stats': stat_list,
            "player_details" : player_details 
        }

