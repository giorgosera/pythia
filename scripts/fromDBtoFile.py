'''
Created on 13 Nov 2011

@author: george

This module accesses a .db file and reads the entries and then write them to a file.
'''

import sqlite3

conn = sqlite3.connect('../../data/cam/cam.db')
cur = conn.cursor()
cur.execute("select username, date, origin, no_followers, message \
             from cambridge_clean_comma")
results = cur.fetchall()
for result in results:
    t = Tweet()
    t.username = result.username
    print t.username
