# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.http import HtmlResponse
body = '''
               <div class="crumbs fl">
				<a href="http://bj.weather.com.cn" target="_blank">北京</a>
				<span>&gt;</span>
				 <span>朝阳</span>
			    </div>
       '''

response = HtmlResponse(url="http://www.example.com",body=body,encoding='utf-8')


#选中所有的img标签
selector = response.css("div>a::text")
print(selector.extract())
selector1 = response.css("div>span:last-child::text").extract()
print(selector1)