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
                   "http://twtrland.com/profile/nprnews",
                   "http://twtrland.com/profile/nytimesphoto",
                   "http://twtrland.com/profile/lemondefr",
                   "http://twtrland.com/profile/guardiannews",
                   "http://twtrland.com/profile/cnnbrk",
                   "http://twtrland.com/profile/nytimesworld",
                   "http://twtrland.com/profile/time",
                   "http://twtrland.com/profile/wired",
                   #Journalists
                   "http://twtrland.com/profile/Kristiturnquist",
                   "http://twtrland.com/profile/colliderfrosty",
                   "http://twtrland.com/profile/kyleveazey",
                   "http://twtrland.com/profile/mattvensel",
                   "http://twtrland.com/profile/richdemuro",
                   "http://twtrland.com/profile/jayrosen_nyu",
                   "http://twtrland.com/profile/Brian_Whit",
                   "http://twtrland.com/profile/Dima_Khatib",
                   "http://twtrland.com/profile/latrive",
                   "http://twtrland.com/profile/ian_black",
                   "http://twtrland.com/profile/jeremyscahill",
                   "http://twtrland.com/profile/bencnn",
                   "http://twtrland.com/profile/ianinegypt",
                   "http://twtrland.com/profile/sultanalqassemi",
                   "http://twtrland.com/profile/mbaa",
                   "http://twtrland.com/profile/sarahraslan",
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
                   "http://twtrland.com/profile/yassayari",
                   "http://twtrland.com/profile/ifikra",
                   "http://twtrland.com/profile/3Beee",
                   "http://twtrland.com/profile/SamarMEZ",
                   "http://twtrland.com/profile/gamaleid",
                   "http://twtrland.com/profile/Tharwacolamus",
                   "http://twtrland.com/profile/weddady",
                   "http://twtrland.com/profile/wael",
                   "http://twtrland.com/profile/djmeddi",
                   "http://twtrland.com/profile/alshaheeed",
                   "http://twtrland.com/profile/justicentric",
                   "http://twtrland.com/profile/exiledsurfer",
                   #Celebrities
                   "http://twtrland.com/profile/BillGates",
                   "http://twtrland.com/profile/TheEllenShow",
                   "http://twtrland.com/profile/ladygaga",
                   "http://twtrland.com/profile/aplusk",
                   "http://twtrland.com/profile/justinbieber",
                   "http://twtrland.com/profile/amywinehouse",
                   "http://twtrland.com/profile/tomhanks",
                   "http://twtrland.com/profile/MMFlint",
                   "http://twtrland.com/profile/billmaher",
                   "http://twtrland.com/profile/SethMacFarlane",
                   "http://twtrland.com/profile/stephenfry",
                   #Commoners
                   "http://twtrland.com/profile/geracleous",
                   "http://twtrland.com/profile/marios",
                   "http://twtrland.com/profile/Nik_Adhia",
                   "http://twtrland.com/profile/Alicebentinck",
                   "http://twtrland.com/profile/ZenonasTziarras",
                   "http://twtrland.com/profile/Lenia_Ev",
                   "http://twtrland.com/profile/alexismic",
                   "http://twtrland.com/profile/alex_diak",
                   "http://twtrland.com/profile/LouiseZd",
                   "http://twtrland.com/profile/LilKalih",
                   "http://twtrland.com/profile/mrad_",
                   "http://twtrland.com/profile/G0rginos",
                   "http://twtrland.com/profile/sonic2000gr",
                   "http://twtrland.com/profile/mariiaanaM"]

    def __init__(self, name=None, **kwargs): 
        BaseSpider.__init__(self,name)
        if kwargs:  
            self.start_urls = [kwargs['user_url']]

    

    def parse(self, response):
        try:
            hxs = HtmlXPathSelector(response)
            item = UserStatsItem()
            title = hxs.select('/html/head/title/text()').extract()
            
            number_pattern = re.compile("[0-9]+")
            name_pattern = re.compile('[a-zA-Z0-9_]*,')
            
            r = name_pattern.findall(str(title))
            item['screen_name'] = r[0].split(',')[0]
            
            followers_section = hxs.select('//div[@class="belowImage"]')[1]
            item['followers'] = int(followers_section.select('b/text()').extract()[0])
            item['friends'] = int(followers_section.select('b/text()').extract()[1]) 
            
            total_tweet_pattern = re.compile("Based on analyzing [0-9]*")
            r = total_tweet_pattern.findall(str(response.body))
            r =  number_pattern.findall(r[0])
            total_tweets = int(r[0]) 
            item['total_tweets'] = total_tweets
            
            retweets_section = hxs.select('//div[@class="aboutContent"]')[2]
            sub = retweets_section.select('b/text()').extract()
            
            if sub[0] != "∞": #infinity symbol 
                item['retweeted'] = float(sub[0])
            else:
                item['retweeted'] = 0.0  
                
            if sub[2] != "∞": #infinity symbol 
                item['retweets'] = 1.0/float(sub[2])
            else:
                item['retweets'] = 0.0
                
            js_section = hxs.select('//div[@class="rightSide"]/script/text()').extract()
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
        except Exception, e:
            print e
            item = UserStatsItem()
            return item