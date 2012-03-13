'''
Created on 25 Jan 2012

@author: george

A small script to escaped HTML characters from the tweet text 
'''

from mongoengine import *
from database.model.tweets import *
import HTMLParser

connect("pythia_db")
t = EgyptTweet.objects.order_by("-date")
size = len(t)
print "min:", t[0].date
print "max:", t[size-1].date

