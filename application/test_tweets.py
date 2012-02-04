'''
Created on 22 Jan 2012

@author: george
'''
import datetime
from crawlers.CrawlerFactory import CrawlerFactory
from database.model.tweets import TwoGroupsTweet
from mongoengine import *

f = CrawlerFactory()
t = f.get_crawler("topsy")

search_hashtags = "uk OR #uk OR #UK or #usa OR #USA OR #US OR usa OR us"
t.search_for(search_hashtags)
t.search_between(from_date=datetime.datetime(2011, 01, 23, 0, 0, 0), 
                 to_date=datetime.datetime(2011, 01, 25, 0, 0, 0), 
                 granularity_days=1, 
                 granularity_hours=0, 
                 granularity_mins=0)
t.retrieve_items_of_type(TwoGroupsTweet)
t.crawl()

