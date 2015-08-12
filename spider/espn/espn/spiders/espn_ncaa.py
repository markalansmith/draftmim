import scrapy
import urlparse
from urllib2 import quote

from espn.items import *

class ESPNSpider(scrapy.Spider):
    name = 'espn_ncaa_hoops'
    allowed_domains = ['espn.go.com']
    start_urls = [
        'http://espn.go.com/mens-college-basketball/teams',
    ]

    def parse(self, response):
        selector = scrapy.Selector(response)
        conference_divs = selector.xpath(
            '//div[@class="mod-container mod-open-list mod-teams-list-medium mod-no-footer"]')
        for conference_div in conference_divs:
            conference_name = conference_div.xpath('.//div[@class="mod-header colhead"]/h4/text()').extract()
            conference_team_divs = conference_div.xpath('.//div[@class="mod-content"]/ul/li')
            for conference_team_div in conference_team_divs:
                team_name = conference_team_div.xpath('.//h5/a/text()').extract()
                team_page = conference_team_div.xpath('.//h5/a/@href').extract()
                team_stats_link, team_schedule_link, team_roster_link = conference_team_div.xpath(
                    './/span/a/@href').extract()
                stats, schedule, roster = conference_team_div.xpath('.//span/a/text()').extract()
                self.logger.info("Conf: %s Team: %s Team Page: %s" % (conference_name, team_name, team_page,))

                team_item = TeamItem()
                team_item['conference'] = conference_name[0].strip()
                team_item['name'] = team_name[0].strip()
                team_item['url'] = team_page[0].strip()
                team_item['stats_url'] = team_stats_link[0].strip()

                # Extend the links from relative paths to full paths
                team_schedule_link = urlparse.urljoin(response.url, team_schedule_link.strip())
                team_roster_link = urlparse.urljoin(response.url, team_roster_link.strip())
                team_stats_link = urlparse.urljoin(response.url, team_stats_link.strip())
                team_page_link = urlparse.urljoin(response.url, team_page[0].strip())
                
                # Update the item with the links
                team_item['url'] = team_page_link
                team_item['stats_url'] = team_stats_link

                # Parse the roster
                roster_request = scrapy.Request(team_roster_link, callback=self.parse_team_roster)
                roster_request.meta['team_item'] = team_item
                yield roster_request

                # Parse the team schedule
                schedule_request = scrapy.Request(team_schedule_link, callback=self.parse_team_schedule)
                schedule_request.meta['team_item'] = team_item
                yield schedule_request


    def parse_team_roster(self, response):
        team_item = response.meta['team_item']
        roster_rows = response.xpath('//div[@class="mod-content"]/table').xpath('./tr')
        roster = []

        for roster_row in roster_rows:
            roster_row_class = roster_row.xpath('./@class').extract()
            if 'row' in roster_row_class[0]:
                player_name = roster_row.xpath('./td/a/text()').extract()
                player_page = roster_row.xpath('./td/a/@href').extract()
                player_details = roster_row.xpath('./td/text()').extract()
                player_number, player_position, player_height, player_weight, player_class, player_hometown = player_details
                player_item = PlayerItem()
                player_item['name'] = player_name[0].strip()
                player_item['number'] = player_number.strip()
                player_item['position'] = player_position.strip()
                player_item['height_ft'] = player_height.strip()
                player_item['year_class'] = player_class.strip()
                player_item['hometown'] = player_hometown.strip()
                player_item['url'] = player_page[0].strip()
                roster.append(player_item)
                self.logger.info('Team: %s, Player: %s, Details: %s' % (team_item['name'], player_name, str(player_details),))

        team_item['roster'] = roster

        if 'games' in team_item:
            yield team_item


    def parse_team_schedule(self, response):
        team_item = response.meta['team_item']
        schedule_table_rows = response.xpath('//div[@class="mod-content"]/table').xpath('./tr')
        scheduled_games = []
        for schedule_row in schedule_table_rows:
            schedule_row_class = schedule_row.xpath('./@class').extract()
            if 'row' in schedule_row_class[0]:
                game_date = schedule_row.xpath('./td/text()').extract()[0]

                # Check if the schedule exists
                if game_date == 'No schedule available.':
                    continue

                game_time = schedule_row.xpath('./td/text()').extract()[1]
                game_opponent = schedule_row.xpath('./td/ul/li[@class="team-name"]/a/text()').extract()
                if not game_opponent:
                    # If the team doesn't have a page, there is no ahref to worry about
                    game_opponent = schedule_row.xpath('./td/ul/li[@class="team-name"]/text()').extract()

                game_home_away = schedule_row.xpath('./td/ul/li[@class="game-status"]/text()').extract()

                game_item = GameItem()
                game_item['game_date'] = game_date.strip()
                game_item['game_time'] = game_time.strip()
                game_item['opponent'] = game_opponent[0].strip()[0]
                game_item['home_away'] = 'away' if game_home_away[0].strip() == '@' else 'home'
                scheduled_games.append(game_item)
                self.logger.info('Team: %s, Game Date: %s, Game Opponent: %s, HomeAway: %s' % (
                    team_item['name'], game_date, game_opponent, game_home_away,))

        team_item['games'] = scheduled_games

        if 'roster' in team_item:
            yield team_item
