# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TeamItem(scrapy.Item):
    name = scrapy.Field()
    conference = scrapy.Field()
    url = scrapy.Field()
    stats_url = scrapy.Field()
    games = scrapy.Field()
    roster = scrapy.Field()

class PlayerItem(scrapy.Item):
    name = scrapy.Field()
    number = scrapy.Field()
    position = scrapy.Field()
    height_ft = scrapy.Field()
    weight_lbs = scrapy.Field()
    year_class = scrapy.Field()
    hometown = scrapy.Field()
    url = scrapy.Field()

class GameItem(scrapy.Item):
    game_date = scrapy.Field()
    game_time = scrapy.Field()
    opponent = scrapy.Field()
    home_away = scrapy.Field()

