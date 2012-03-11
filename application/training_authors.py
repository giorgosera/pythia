'''
Created on 22 Jan 2012

@author: george
'''
import datetime
from crawlers.CrawlerFactory import CrawlerFactory
from database.model.tweets import *
from database.model.agents import *
from mongoengine import *
import tools.utils
from urlparse import urlparse
from database.warehouse import WarehouseServer

f = CrawlerFactory()
twitter = f.get_crawler("twitter")
#twitter.login()
ws = WarehouseServer()

from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
to_date = datetime.datetime(2011, 1, 26, 0, 00, 0) 
items = ws.get_documents_by_date(from_date, to_date, limit=100)  
screen_names = []
for tweet in items:
    screen_names.append(tweet.author_screen_name)
screen_names = set(screen_names)
print len(screen_names)
# A terrible hack to save the screen_names of users which are mentioned in tweets 
# but they are not yet in the database. They'll be considered after all authors have 
#been stored.
mentions_of_not_stored_users = [] 

for author_name in screen_names:        
        author = Author.objects(screen_name=author_name) 
        if len(author) == 0: #If not in db yet
            tweets = EgyptTweet.objects(author_screen_name=author_name)
            author = Author()
            author.screen_name = author_name
            author.followers_count = 0 
            author.friends_count = 0
            author.tweets = tweets
            for tweet in tweets:
                #If the url belongs to that user then this is their tweet so theri retweets as well
                if author_name == urlparse(tweet.url).path.split('/')[1]:
                    author.retweeted_tweets += tweet.retweet_count
                urls = tools.utils.extract_urls(tweet.content.raw)
                if len(urls) > 0 : #We just want to find out if this tweet has aurl not how many
                    author.links += 1 
                
                #if this is a retweet increase counter
                if tools.utils.is_a_retweet(tweet.content.raw):    
                    author.retweets += 1 
                else: #We don't take @ in retweets as mentions or replies
                    #if this is a mention to another user then increase replies
                    #counter and also update the mentioned user's mentions
                    mentions = tools.utils.get_mentions(tweet.content.raw)
                    if len(mentions) > 0:
                        author.replies_to_others += 1 #No matter how many people are mentioned in the tweet we just increase by one cz we just want to know if this tweet is a reply 
                        for mention in mentions:
                            mentioned_author = Author.objects(screen_name=mention)
                            if len(mentioned_author) > 0:
                                ma = mentioned_author.get() 
                                ma.mentions_by_others += 1
                                ma.save()
                            else:
                                mentions_of_not_stored_users.append(mention)
            author.save()
        else:
            pass
            #TODO: If already stored then either do nothing or if followers and friends empty then ask API

print mentions_of_not_stored_users

for author in Author.objects():
    print '--------------------------------'
    print 'screen_name: ', author.screen_name     
    print 'followers: ', author.followers_count     
    print 'followees: ', author.friends_count
   
    for tweet in author.tweets:
        print tweet.content.raw
        print tweet.url
        print tweet.retweet_count
       
    print 'tweets: ', author.tweets
    print 'retweets: ', author.retweets     
    print 'retweeted: ', author.retweeted_tweets              
    print 'links: ', author.links              
    print 'replies: ', author.replies_to_others              
    print 'mentions: ', author.mentions_by_others       


#===============================================================================
# for tweet in TrainingTweet.objects:
#   screen_name = tweet.author_screen_name
#   if TrainingAuthor.objects(screen_name=screen_name) == None:
#       author = TrainingAuthor()
#       basic_info = twitter.get_user_info_by_screenname(screen_name)
#       author.followers_count = basic_info["followers_count"]
#       author.friends_count = basic_info["friends_count"]
#      
#      
#   else:
#       author = Author.objects(screen_name=screen_name).get()
#===============================================================================
