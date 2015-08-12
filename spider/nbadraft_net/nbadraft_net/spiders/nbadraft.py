# -*- coding: utf-8 -*-
import scrapy
import urlparse
from urllib2 import quote

from nbadraft_net import PlayerItem


class NbadraftSpider(scrapy.Spider):
    name = "nbadraft"
    allowed_domains = ["nbadraft.net"]
    start_urls = (
        'http://www.nbadraft.net/2016mock_draft',
    )

    def parse(self, response):
        selector = scrapy.Selector(response)
        updated_on = selector.xpath('//p[@class="updated"]/text()').extract()[0]
        mock_draft_one = selector.xpath('//div[@id="nba_consensus_mock1"]')
        mock_draft_two = selector.xpath('//div[@id="nba_consensus_mock2"]')

        for mock_draft in [mock_draft_one, mock_draft_two]:
            player_rows = mock_draft.xpath('.//table/tbody/tr')
            for player_row in player_rows:
                player_item = PlayerItem()

                player_info = player_row.xpath('./td/text()').extract()

                player_name = player_row.xpath('./td/a/text()').extract()[0]
                player_page = player_row.xpath('./td/a/@href').extract()[-1]
                
                player_page_url = urlparse.urljoin(response.url, player_page.strip())
                player_page_request = scrapy.Request(player_page_url, callback=self.parse_player_page_request)

                player_mock_draft_pos = int(player_info[0])
                player_height = player_info[2]
                player_weight = int(player_info[3])
                player_position = player_info[4]
                player_school = player_info[5]
                player_class = player_info[6]

                player_item['name'] = player_name

                self.logger.info("PlayerInfo: %s, Player Name: %s, Player Page: %s" % (str(player_info), player_name, str(player_page_request),))
                yield player_page_request

    def parse_player_page_request(self, response):
        selector = scrapy.Selector(response)
        
        player_stats = selector.xpath('//div[@id="nba_player_stats"]')
        player_img_src = player_stats.xpath('./img/@src').extract()
        player_attribute_scores = selector.xpath('//p[@class="nba_player_attrib_score"]/text()').extract()
        player_overall_score = selector.xpath('//p[@class="whitebox"]/text()').extract()
 	player_notes = selector.xpath('//div[@id="nbap_content_bottom"]/p/text()').extract()
        player_videos = selector.xpath('//div[@id="nbap_content_bottom"]/p/iframe/@src').extract()
        
        return
                
