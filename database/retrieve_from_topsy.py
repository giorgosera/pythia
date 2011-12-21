'''
Created on 13 Nov 2011

@author: george

This module utilizes the Otter API bindings for Python to retrieve old tweets.
'''
import otter #!@UnresolvedImport
import dateutil.parser, datetime
import time
from model.tweets import TopsyTweet
from model.agents import Author
from mongoengine import connect
from crawlers.CrawlerFactory import CrawlerFactory

PAGE_SIZE = 100

connect("pythia_db")

mintime = datetime.datetime(2011, 01, 01, 0, 0, 0)
delta = datetime.timedelta(hours=12)
maxtime = mintime + delta
final_date = datetime.datetime(2011, 02, 15, 0, 0, 0)
count = 0
while maxtime != final_date:
    for page in range(PAGE_SIZE):        
        search = otter.Resource('search')
        search(q='#jan25 OR #egypt OR #tahrir', mintime = time.mktime(mintime.timetuple()), maxtime = time.mktime(maxtime.timetuple()), type='tweet', offset=page*10)
        #for res in search.response.list:
            #print res.content
        print search.response.list.url
        mintime = maxtime
        maxtime += delta
print "Total:", count            

        
#===============================================================================
# r = otter.Resource('searchdate')
# r(q='#egypt', window='a', type='tweet')
# 
# print "Initialising Twitter crawler object..."
# factory = CrawlerFactory()
# t = factory.get_crawler("twitter")
# t.login()
# count = 0
#===============================================================================
        
#===============================================================================
# for page in r:
#    for i in page.response.list:
#        print count
#        count += 1        
# print "count",count        
#===============================================================================
#===============================================================================
# print "Retrieving tweets from Topsy..."
# count = 0 
# for page in r:
#    for item in page.response.list:
#        print "Storing tweet #",count
#        tt = TopsyTweet()
#        tt.url = item.url
#        tt.text = item.content
#        formatted_date = datetime.datetime.fromtimestamp(item.date).strftime('%Y-%m-%d %H:%M:%S')
#        tt.date = dateutil.parser.parse(formatted_date)
#        tt.screen_name = item.trackback_author_nick
#        tt.save(safe=True)        
#        
#        print "Storing author info for this tweet!"    
#        at = Author()
#        try:
#            info = t.get_user_info_by_screenname(tt.screen_name)
#            at.twitter_id = info['id']
#            at.screen_name = info['screen_name']
#            at.followers_ids = t.get_user_followers(at.screen_name)
#            at.friends_ids = t.get_user_friends(at.screen_name)
#            at.followers_count = info['followers_count']
#            at.friends_count = info['friends_count']
#            at.statuses_count = info['statuses_count']
#            at.location = info['location']
#        except Exception, e:
#            at.screen_name = "UserNotFound"
#        finally:
#            at.save(safe=True)    
#        
#        count += 1    
# print "Succesfully retrieved tweets!"    
#===============================================================================