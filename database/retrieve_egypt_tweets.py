'''
Created on 13 Nov 2011

@author: george

This module utilizes the Otter API bindings for Python to retrieve old tweets.
'''
import otter #!@UnresolvedImport
import datetime
import time
from model.tweets import EgyptTweet
from mongoengine import connect

PAGE_SIZE = 10

connect("pythia_db")

#The old retrievals were between 1/1/2011 and 15/2/2011 (3 hours)
mintime = datetime.datetime(2011, 01, 23, 0, 0, 0)
delta = datetime.timedelta(hours=1)
maxtime = mintime + delta
final_date = datetime.datetime(2011, 01, 27, 0, 0, 0)

exception_log = []

search_hashtags = "#25jan OR #jan25 OR #egypt OR #tahrir OR #fuckmubarak OR #mubarak \
                   OR #suez OR #DownWithMubarak OR #NOSCAF OR #SCAF OR #cairo"

kw = otter.loadrc() # load api key

count = 0
while maxtime != final_date:
    for page in range(PAGE_SIZE):        
        try:
            search = otter.Resource('search', **kw)
            #search(q='#jan25 OR #egypt OR #tahrir', mintime = time.mktime(mintime.timetuple()), maxtime = time.mktime(maxtime.timetuple()), type='tweet', offset=page*10)
            search(q=search_hashtags, mintime = time.mktime(mintime.timetuple()), maxtime = time.mktime(maxtime.timetuple()), type='tweet', perpage=100, page=page+1)
            for item in search.response.list:
                print "Storing tweet #",count, "for the period",mintime,"until",maxtime 
                tt = EgyptTweet()
                tt.url = item.url
                tt.content = item.content
                tt.date = mintime
                tt.screen_name = item.trackback_author_nick
                tt.retweet_count = item.trackback_total
                tt.author_screen_name = item.trackback_author_nick
                tt.author_name = item.trackback_author_name
                print tt.url
                print tt.author_name
                tt.save(safe=True)
                count += 1     
        except Exception, e:
            print e
            exception_log.append(e)
        finally:
            pass          
    print tt.url        
    print "Retrieving tweets for next three hours"         
    mintime = maxtime
    maxtime += delta
        
print "Succesfully retrieved", count,"tweets!"    
print "Exceptions:"    
for e in exception_log:
    print e

#HTTP Error 503: Credit Limit Reached
#formatted_date = datetime.datetime.fromtimestamp(item.date).strftime('%Y-%m-%d %H:%M:%S')        
#tt.date = dateutil.parser.parse(formatted_date)
#========================================================================
# print "Storing author info for this tweet!"    
# at = Author()
# try:
#    info = t.get_user_info_by_screenname(tt.screen_name)
#    at.twitter_id = info['id']
#    at.screen_name = info['screen_name']
#    at.followers_ids = t.get_user_followers(at.screen_name)
#    at.friends_ids = t.get_user_friends(at.screen_name)
#    at.followers_count = info['followers_count']
#    at.friends_count = info['friends_count']
#    at.statuses_count = info['statuses_count']
#    at.location = info['location']
# except Exception, e:
#    at.screen_name = "UserNotFound"
# finally:
#    at.save(safe=True)    
# 
# count += 1    
#========================================================================
