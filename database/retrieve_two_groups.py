'''
Created on 13 Nov 2011

@author: george

This module utilizes the Otter API bindings for Python to retrieve old tweets.
'''
import otter #!@UnresolvedImport
from model.tweets import PsychTweet
from mongoengine import connect

PAGE_SIZE = 100

connect("pythia_db")

count = 0
exception_log = []

users = ["debatespsych", "psychissues", "chatpsych"]

kw = otter.loadrc() # load api key
for user in users:
    for page in range(PAGE_SIZE):        
        try:
            search = otter.Resource('linkposts', **kw)
            search(url="http://twitter.com/"+user, type='tweet', perpage=10, page=page+1)
            for item in search.response.list:
                print "Storing tweet #",count, "for the user",user 
                print item
                count += 1     
        except Exception, e:
            print e
            exception_log.append(e)
        finally:
            pass          
    print "Retrieving tweets for next user"         
        
print "Succesfully retrieved", count,"tweets!"    
print "Exceptions:"    
for e in exception_log:
    print e