'''
Created on 13 Nov 2011

@author: george

This module utilizes the Otter API bindings for Python to retrieve old tweets.
'''
import otter #!@UnresolvedImport
import dateutil.parser, datetime
from model.tweets import TopsyTweet
from model.agents import Author
from mongoengine import connect
from crawlers.CrawlerFactory import CrawlerFactory

connect("pythia_db")

r = otter.Resource('searchdate')
r(q='#egypt', window='a', type='tweet')

print "Initialising Twitter object..."
factory = CrawlerFactory()
t = factory.get_crawler("twitter")
t.login()


print "Retrieving tweets from Topsy..."
count = 0 
for page in r:
    for item in page.response.list:
        print "Storing tweet #",count
        tt = TopsyTweet()
        tt.url = item.url
        tt.text = item.content
        formatted_date = datetime.datetime.fromtimestamp(item.date).strftime('%Y-%m-%d %H:%M:%S')
        tt.date = dateutil.parser.parse(formatted_date)
        tt.screen_name = item.trackback_author_nick
        tt.save(safe=True)        
        
        print "Storing author info for this tweet!"    
        at = Author()
        try:
            info = t.getUserInfoByScreenName(tt.screen_name)
            at.screen_name = info['screen_name']
            at.followers_count = info['followers_count']
            at.friends_count = info['friends_count']
            at.statuses_count = info['statuses_count']
            at.location = info['location']
        except Exception, e:
            at.screen_name = "UserNotFound"
        finally:
            at.save(safe=True)    
        
        count += 1    
print "Succesfully retrieved tweets!"    