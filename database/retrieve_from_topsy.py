'''
Created on 13 Nov 2011

@author: george

This module utilizes the Otter API bindings for Python to retrieve old tweets.
'''
import otter, dateutil.parser, datetime
from model.tweets import TopsyTweet
from mongoengine import connect

connect("pythia_db")

r = otter.Resource('searchdate')
r(q='#egypt#mubarak', window='a', type='tweet')
for page in r:
    for item in page.response.list:
        tt = TopsyTweet()
        tt.hits = item.hits
        tt.title = item.title
        tt.url = item.url
        tt.highlight = item.highlight
        tt.text = item.content
        formatted_date = datetime.datetime.fromtimestamp(item.date).strftime('%Y-%m-%d %H:%M:%S')
        tt.date = dateutil.parser.parse(formatted_date)
        tt.trackback_total = item.trackback_total
        tt.trackback_author_url = item.trackback_author_url
        tt.trackback_permalink = item.trackback_permalink
        tt.topsy_author_url = item.topsy_author_url
        tt.username = item.trackback_author_nick
        tt.save()
    