# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyWeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weather_text = scrapy.Field()
    city_code = scrapy.Field()
    city_name = scrapy.Field()
