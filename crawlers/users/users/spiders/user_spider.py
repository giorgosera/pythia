import re
from scrapy.spider import BaseSpider#!@UnresolvedImport
from scrapy.selector import HtmlXPathSelector#!@UnresolvedImport
from users.items import UserStatsItem#!@UnresolvedImport

class UserSpider(BaseSpider):
    name = "user_stats"
    allowed_domains = ["twtrland.com"]
    start_urls = ["http://twtrland.com/update/profile/geracleous", "http://twtrland.com/update/profile/aplusk"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        item = UserStatsItem()
        followers_section = hxs.select('//div[@class="belowImage"]')[1]
        item['followers'] = followers_section.select('b/text()').extract()[0]
        item['friends'] = followers_section.select('b/text()').extract()[1] 
        total_tweets = followers_section.select('b/text()').extract()[2]
    
        retweets_section = hxs.select('//div[@class="aboutContent"]')[2]
        sub = retweets_section.select('b/text()').extract()
        item['retweeted'] = sub[0]	
        item['retweets'] = 1.0/float(sub[2])
    
        js_section = hxs.select('//div[@class="rightSide"]/script/text()').extract()
        number_pattern = re.compile("[0-9]+")
        pattern = re.compile("numOfConversations =[\s]*[0-9]*")
        r = pattern.findall(str(js_section))	
        r = number_pattern.findall(r[1])
        item['replies'] = float(r[0])/float(total_tweets)
    
        pattern = re.compile("numOfLinks =[\s]*[0-9]*")
        r = pattern.findall(str(js_section))
        r = number_pattern.findall(r[1])
        item['links'] = float(r[0])/float(total_tweets)
    
        pattern = re.compile("numOfMentions =[\s]*[0-9]*")
        r = pattern.findall(str(js_section))
        r = number_pattern.findall(r[1])
        item['mentions'] = float(r[0])/float(total_tweets)
        
        return item