'''
Created on 25 Jan 2012

@author: george

A small script to escaped HTML characters from the tweet text 
'''

from mongoengine import *
from database.model.tweets import *
import HTMLParser

connect("pythia_db")
for t in EgyptTweet.objects:
    print t.content
    t.content = HTMLParser.HTMLParser().unescape(t.content)
    print t.content
    t.save()
print "All tweets are clear."
     

