'''
Created on 13 Nov 2011

@author: george

This module accesses a .db file and reads the entries and then write them to a file.
'''

import sqlite3, dateutil.parser
from model.tweets import Tweet
from mongoengine import connect

connect("pythia_db")

conn = sqlite3.connect('../../data/cam/cam.db')
cur = conn.cursor()
cur.execute("select username, date, origin, no_followers, message \
             from cambridge_clean_comma")

results = cur.fetchall()
for result in results:
    t = Tweet()
    t.username = result[0]
    t.date = dateutil.parser.parse(result[1])
    t.origin = result[2]
    t.no_of_followers = result[3]
    t.text = result[4]
    t.source = "cambridge"
    t.save()
    
    
    
    
    
    