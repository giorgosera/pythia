'''
Created on 13 Nov 2011

@author: george

This module accesses a .db file and reads the entries and then write them to a file.
'''

import sqlite3, dateutil.parser
from model.tweets import CambridgeTweet
from mongoengine import connect

connect("pythia_db")

conn = sqlite3.connect('../../data/cam/cam.db')
cur = conn.cursor()
cur.execute("select username, date, origin, no_followers, message \
             from cambridge_clean_comma")

results = cur.fetchall()
for result in results:
    ct = CambridgeTweet()
    ct.from_user = result[0]
    ct.date = dateutil.parser.parse(result[1])
    ct.origin = result[2]
    ct.no_of_followers = result[3]
    ct.text = result[4]
    ct.save()

    
    
    
    
    
    