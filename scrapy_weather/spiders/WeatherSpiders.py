# -*- coding: utf-8 -*-
import re

import scrapy


#爬取天气 存储到db
from scrapy_weather.items import ScrapyWeatherItem


class WeatherSpiders(scrapy.Spider):
    name = "weather"
    start_url = [
        "http://www.weather.com.cn/",
    ]
    municipality = [
                     'http://bj.weather.com.cn/',
                     'http://sh.weather.com.cn/',
                     'http://tj.weather.com.cn/',
                     'http://cq.weather.com.cn/',
                 ],
    urls_type1 = [
        'http://bj.weather.com.cn/',
        'http://sh.weather.com.cn/',
        'http://tj.weather.com.cn/',
        'http://cq.weather.com.cn/',
        'http://hebei.weather.com.cn/',
        'http://henan.weather.com.cn/',
        'http://sd.weather.com.cn/',
        'http://shanxi.weather.com.cn/',
        'http://shaanxi.weather.com.cn/',
        'http://js.weather.com.cn/',
        'http://hunan.weather.com.cn/',
        'http://hubei.weather.com.cn/',
        'http://ah.weather.com.cn/',
        'http://zj.weather.com.cn/',
        'http://jx.weather.com.cn/',
        'http://fj.weather.com.cn/',
        'http://mo.weather.com.cn/',
    ],
    urls_type2 = [
        'http://gd.weather.com.cn/',
        'http://gx.weather.com.cn/',
        'http://hainan.weather.com.cn/',
        'http://yn.weather.com.cn/',
        'http://gz.weather.com.cn/',
        'http://sc.weather.com.cn/',
        'http://xz.weather.com.cn/',
        'http://xj.weather.com.cn/',
        'http://qh.weather.com.cn/',
        'http://gs.weather.com.cn/',
        'http://nx.weather.com.cn/',
        'http://nmg.weather.com.cn/',
        'http://hlj.weather.com.cn/',
        'http://jl.weather.com.cn/',
        'http://ln.weather.com.cn/',
    ]



    #开始url


    #开始页面
    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)

    def start_requests(self):
        yield scrapy.Request(self.start_url[0], callback=self.parse_provice)


    #解析省
    def parse_provice(self,response):
        sel = response.xpath('/html/body/div[1]/div[3]/ul[7]/li[1]/a[1]/@href').extract_first()
        yield scrapy.Request(sel, callback=self.parse_city)

    #解析城市列表（包括直辖市和省份）
    def parse_city(self, response):
        selList = response.xpath('/html/body/div[2]/div[2]/ul/li/a/@href')
        for sel in selList:
            url = sel.extract()
            # 过滤掉错误连接
            if 'www.weather.com.cn/html/province/' not in url:
                if(self.isUrlTypeOne(url)):
                    yield scrapy.Request(url, callback=self.parse_citytype1)
                elif(self.isUrlTypeTwo(url)):
                    yield scrapy.Request(url, callback=self.parse_citytype2)

    def parse_citytype1(self,response):

        base_url = response.url
        #直辖市列表
        if(self.is_municipality(base_url)):
            citylist = response.xpath('/html/body/div[1]/div[2]/div/span/a/@href')
            for cel in citylist:
                fetchurl = cel.extract()
                yield scrapy.Request(fetchurl, callback=self.parse)
        else:
            citylist = response.xpath('/html/body/div[1]/div[2]/div/span/a/@href')
            for sel in citylist:
                city_url = base_url + sel.extract()
                yield scrapy.Request(city_url, callback=self.parse_everycity)



    #解析除了直辖市之外的每个城市，获取fetch_url
    def parse_everycity(self,response):
        citylist = response.xpath('/html/body/div[1]/div[3]/div/span/a/@href')
        for cel in citylist:
            fetch_url = cel.extract()
            yield scrapy.Request(fetch_url, callback=self.parse)

    def parse_citytype2(self,response):

        base_url = response.url
        citylist = response.xpath('/html/body/div[2]/ul/li/a/@href')
        for sel in citylist:
            #获取a标签的href 和text
            city_url = base_url + sel.extract()
            yield scrapy.Request(city_url, callback=self.parse_everycity)



    #通过城市code获取城市的数据，具体的页面
    '''
    def fetch_weather_bycode(self,response):

        weather = response.xpath('//*[@id="hidden_title"]/@value')
        weather_info = weather.extract_first()
        print("天气数据：" + weather_info)

        city =  response.xpath('/html/body/div[5]/div[1]/div[1]/div[1]')
        city_info = city[0].css("div>a::text").extract_first() + city[0].css("div>span:last-child::text").extract_first()
        #TODO 获取具体的城市 和区域
        print("城市数据：" + city_info)

        city_code = re.findall(r"\d+\d*",str(response.url))

        city = ScrapyWeatherItem()
        city['weather_text'] = weather_info
        city['city_code'] = city_code[0]
        city['city_name'] = city_info
        return city
    '''

    def parse(self, response):
        weather = response.xpath('//*[@id="hidden_title"]/@value')
        weather_info = weather.extract_first()
        city = response.xpath('/html/body/div[5]/div[1]/div[1]/div[1]')
        city_info = city[0].css("div>a::text").extract_first() + city[0].css(
            "div>span:last-child::text").extract_first()
        city_code = re.findall(r"\d+\d*", str(response.url))

        city = ScrapyWeatherItem()
        city['weather_text'] = weather_info
        city['city_code'] = city_code[0]
        city['city_name'] = city_info

        return city


    #TODO 下面两个方法加个type字段可以抽成一个方法
    #类型2的url 【广州---辽宁】
    def isUrlTypeTwo(self, url):

        for str in self.urls_type2:
            if (url in str):
                return True

        return False


    #类型1的url 【北京--澳门】
    def isUrlTypeOne(self,url):

        for str in self.urls_type1:
            if(url in str):
                return True

        return False

    def is_municipality(self,url):
        for str in self.municipality:
            if(url in str):
                return True

        return False

