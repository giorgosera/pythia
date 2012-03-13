'''
Created on 22 Jan 2012

@author: george
'''
import json
import os
from pprint import pprint
os.chdir("/home/george/virtualenvfyp/pythia/src/crawlers/users/")
if os.path.exists('/home/george/virtualenvfyp/pythia/src/crawlers/users/items.json'):
    os.remove('/home/george/virtualenvfyp/pythia/src/crawlers/users/items.json')
os.system('scrapy crawl user_stats -o items.json -t json')
json_data=open("/home/george/virtualenvfyp/pythia/src/crawlers/users/items.json")
data = json.load(json_data)
for d in data:
    print d
#===============================================================================
# pprint(data)
# json_data.close()
# print raw_input("What type of user " + "a" + " is?")
#===============================================================================