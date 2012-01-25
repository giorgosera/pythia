'''
Created on 25 Jan 2012

@author: george

A small script to escaped HTML characters from the tweet text 
'''

from mongoengine import *
from database.model.tweets import *
import HTMLParser

connect("pythia_db")
for t in TopsyTweet.objects:
    print t.text
    t.text = HTMLParser.HTMLParser().unescape(t.text)
    print t.text
    t.save()
print "All tweets are clear."
     

