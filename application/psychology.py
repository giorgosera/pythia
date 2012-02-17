'''
Created on 22 Jan 2012

@author: george
'''
import datetime, os
from crawlers.CrawlerFactory import CrawlerFactory
from mongoengine import *
from database.model.agents import *
   
author_names = ["speakingpsyc", "debatespsych", "chatpsych", "discusspsych", "psychissues", "lets_talkpsych", "inspirepsych", "SpeakPsych"] 

f = CrawlerFactory()
t = f.get_crawler("twitter")
t.login()

for author_name in author_names:
    print 'Storing info for', author_name
    #if user doesn't exist in db
    if Author.objects(screen_name=author_name) == None:
        author = Author()
        author.screen_name = author_name
    else:
        author = Author.objects(screen_name=author_name).get()

    followers = t.get_user_followers(author_name)
    friends= t.get_user_friends(author_name)
    author.followers_count = len(followers)
    author.friends_count = len(friends)
    followersh = History()
    followersh.count = len(followers)
    followersh.date = datetime.datetime.utcnow()
    author.followers_history.append(followersh)
    friendsh = History()
    friendsh.count = len(friends)
    friendsh.date = datetime.datetime.utcnow()
    author.friends_history.append(friendsh)
    author.followers_ids = followers
    author.save()
print 'Stored all authors\' info'
    


        