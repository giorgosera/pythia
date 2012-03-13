# -*- coding: utf-8 -*-
import re
from scrapy.spider import BaseSpider#!@UnresolvedImport
from scrapy.selector import HtmlXPathSelector#!@UnresolvedImport
from users.items import UserStatsItem#!@UnresolvedImport

class UserSpider(BaseSpider):
    name = "user_stats"
    allowed_domains = ["twtrland.com"]
    start_urls = [#Media
                  "http://twtrland.com/profile/TheIndyNews",
                  "http://twtrland.com/profile/BBCWorld",
                  "http://twtrland.com/profile/SkyNews",
                   "http://twtrland.com/profile/CNN",
                   "http://twtrland.com/profile/nytimes",
                   "http://twtrland.com/profile/MailOnline",
                   "http://twtrland.com/profile/TelegraphNews",
                   "http://twtrland.com/profile/USATODAY",
                   "http://twtrland.com/profile/el_pais",
                   "http://twtrland.com/profile/AJEnglish",
                   "http://twtrland.com/profile/WSJ",
                   "http://twtrland.com/profile/washingtonpost",
                   "http://twtrland.com/profile/timesofindia",
                   "http://twtrland.com/profile/Hurriyet",
                   #Journalists
                   "http://twtrland.com/profile/Kristiturnquist",
                   "http://twtrland.com/profile/colliderfrosty",
                   "http://twtrland.com/profile/kyleveazey",
                   "http://twtrland.com/profile/mattvensel",
                   "http://twtrland.com/profile/richdemuro",
                   "http://twtrland.com/profile/jayrosen_nyu",
                   #Activists
                   "http://twtrland.com/profile/alkoga",
                   "http://twtrland.com/profile/alaa",
                   "http://twtrland.com/profile/Gsquare86",
                   "http://twtrland.com/profile/Esraa2008",
                   "http://twtrland.com/profile/kamalkhalil20",
                   "http://twtrland.com/profile/KareemAmer",
                   "http://twtrland.com/profile/maikelnabil",
                   "http://twtrland.com/profile/monaeltahawy",
                   "http://twtrland.com/profile/Monasosh",
                   "http://twtrland.com/profile/Ghonim",
                   #Celebrities
                   "http://twtrland.com/profile/BillGates",
                   "http://twtrland.com/profile/TheEllenShow",
                   "http://twtrland.com/profile/ladygaga",
                   "http://twtrland.com/profile/aplusk",
                   "http://twtrland.com/profile/justinbieber",
                   "http://twtrland.com/profile/amywinehouse",
                   "http://twtrland.com/profile/tomhanks",
                   #Commoners
                   "http://twtrland.com/profile/geracleous",
                   "http://twtrland.com/profile/marios",
                   "http://twtrland.com/profile/Nik_Adhia",
                   "http://twtrland.com/profile/Alicebentinck",
                   "http://twtrland.com/profile/ZenonasTziarras",
                   "http://twtrland.com/profile/Lenia_Ev",
                   "http://twtrland.com/update/profile/alexismic"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        item = UserStatsItem()
        title = hxs.select('/html/head/title/text()').extract()
        name_pattern = re.compile('[a-zA-Z0-9_]*,')
        r = name_pattern.findall(str(title))
        item['screen_name'] = r[0].split(',')[0]
        followers_section = hxs.select('//div[@class="belowImage"]')[1]
        item['followers'] = followers_section.select('b/text()').extract()[0]
        item['friends'] = followers_section.select('b/text()').extract()[1] 
        total_tweets = followers_section.select('b/text()').extract()[2]
    
        retweets_section = hxs.select('//div[@class="aboutContent"]')[2]
        sub = retweets_section.select('b/text()').extract()
        
        if sub[0] != "∞": #infinity symbol 
            item['retweeted'] = sub[0]
        else:
            item['retweeted'] = 0.0  
            
        if sub[2] != "∞": #infinity symbol 
            item['retweets'] = 1.0/float(sub[2])
        else:
            item['retweets'] = 0.0
            
        js_section = hxs.select('//div[@class="rightSide"]/script/text()').extract()
        number_pattern = re.compile("[0-9]+")
        pattern = re.compile("numOfConversations =[\s]*[0-9]*")
        if len(js_section) > 0:
            r = pattern.findall(str(js_section))	
        else:
            r = pattern.findall(response.body)

        r = number_pattern.findall(r[1])
        item['replies'] = float(r[0])/float(total_tweets)
    
        pattern = re.compile("numOfLinks =[\s]*[0-9]*")
        if len(js_section) > 0:
            r = pattern.findall(str(js_section))    
        else:
            r = pattern.findall(response.body)
        r = number_pattern.findall(r[1])
        item['links'] = float(r[0])/float(total_tweets)
    
        pattern = re.compile("numOfMentions =[\s]*[0-9]*")
        if len(js_section) > 0:
            r = pattern.findall(str(js_section))    
        else:
            r = pattern.findall(response.body)
        r = number_pattern.findall(r[1])
        item['mentions'] = float(r[0])/float(total_tweets)
        
        return item