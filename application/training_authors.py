'''
Created on 22 Jan 2012

@author: george
'''
import json
import os
from pprint import pprint
os.chdir("/home/george/virtualenvfyp/pythia/src/crawlers/users/")
os.system('scrapy crawl user_stats -o items.json -t json')
json_data=open("/home/george/virtualenvfyp/pythia/src/crawlers/users/items.json")
data = json.load(json_data)
pprint(data)
json_data.close()