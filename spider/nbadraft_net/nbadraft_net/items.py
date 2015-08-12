# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PlayerItem(scrapy.Item):
    name = scrapy.Field()
    team = scrapy.Field()
    last_update = scrapy.Field()
    url = scrapy.Field()
    draft_pos = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    position = scrapy.Field()
    school = scrapy.Field()
    year_class = scrapy.Field()

    img_src = scrapy.Field()
    athleticism = scrapy.Field()
    size = scrapy.Field()
    defense = scrapy.Field()
    strength = scrapy.Field()
    quickness = scrapy.Field()
    leadership = scrapy.Field()
    jump_shot = scrapy.Field()
    nba_ready = scrapy.Field()
    ball_handling = scrapy.Field()
    potential = scrapy.Field()
    passing = scrapy.Field()
    intangibles = scrapy.Field()

    overall_score = scrapy.Field()

    videos = scrapy.Field()
    
    

