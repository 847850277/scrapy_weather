# -*- coding: utf-8 -*-

import re
from lxml import etree
import requests

f = open('city_code.txt', 'r')
code = f.read()
f.close()


def get_city_code(city):
    pattern = 'name="{}" weatherCode="(.*?)"/>'.format(city)
    city_code = re.findall(pattern, code, re.S)[0]
    return city_code



def get_html(city_code):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' +
                       'Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'}
    url = 'http://www.weather.com.cn/weather/{}.shtml'.format(city_code)
    html = requests.get(url, headers=header)
    html.encoding = 'utf-8'
    print(html.text)
    return html.text


def get_weather(html):
    print(type(html))
    print(dir(html))
    print(html.values)
    for i in range(1, 8):
        date = html.xpath('//*[@id="7d"]/ul/li[{}]/h1/text()'.format(i))[0]
        weather = html.xpath('//*[@id="7d"]/ul/li[{}]/p[1]/text()'.format(i))[0]

        if i == 1:
            temp = html.xpath('//*[@id="7d"]/ul/li[{}]/p[2]/i/text()'.format(i))[0]
        else:
            temp1 = html.xpath('//*[@id="7d"]/ul/li[{}]/p[2]/span/text()'.format(i))[0]
            temp2 = html.xpath('//*[@id="7d"]/ul/li[{}]/p[2]/i/text()'.format(i))[0]
            temp = temp1 + '/' + temp2

        #wind1 = html.xpath('//*[@id="7d"]/ul/li[{}]/p[3]/em/span/@title'.format(i))
        #wind2 = html.xpath('//*[@id="7d"]/ul/li[{}]/p[3]/i/text()'.format(i))
        # if i != 1:
        #     if wind1[0] == '无持续风向':
        #         wind = wind1[1] + ' ' + wind2[0]
        #     elif wind1[1] == '无持续风向':
        #         wind = wind1[0] + ' ' + wind2[0]
        #     else:
        #         wind = wind1[0] + '转' + wind1[1] + ' ' + wind2[0]
        # else:
        #     wind = wind1[0] + ' ' + wind2[0]

        print(date, weather, temp)


def main():
    print('\n\t\t>>>chouyang天气查询<<<\t\t\n\n数据来源:中国天气网(http://www.weather.com.cn/)\n注:仅用于个人练习,绝无商业用途\n')
    city = raw_input('请输入您要查询的城市：(例如:北京)')
    print("输入城市:" + city);
    if re.search(city, code):
        city_code = get_city_code(city)
        print("city code:" + city_code)
        html = etree.HTML(get_html(city_code))
        get_weather(html)

    else:
        print('城市名称有误')
        return None


if __name__ == '__main__':
    main()