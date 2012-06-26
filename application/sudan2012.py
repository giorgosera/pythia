'''
Created on 22 Jan 2012

@author: george
'''
import datetime, os
from crawlers.CrawlerFactory import CrawlerFactory
from database.model.tweets import SudanTweet
from analysis.index import Index
from database.warehouse import WarehouseServer

BASE_PATH = os.path.expanduser("~/virtualenvfyp/pythia/data/")
ws = WarehouseServer()
index_path = os.path.join(BASE_PATH,"sudan_index")
if not os.path.exists(index_path):
    try:
        os.makedirs(index_path)
    except os.error:
        raise Exception(index_path + " could not be created.")  
    
#Save the tweets in the db
f = CrawlerFactory()
t = f.get_crawler("topsy")

search_hashtags = "#sudan OR sudan OR #sudanrevolts OR sudanrevolts"
t.search_for(search_hashtags)
from_date=datetime.datetime(2012, 06, 25, 0, 0, 0)
to_date=datetime.datetime(2012, 06, 26, 14, 30, 0)
t.search_between(from_date=from_date, 
                 to_date=to_date, 
                 granularity_days=0, 
                 granularity_hours=0, 
                 granularity_mins=25)
t.retrieve_items_of_type(SudanTweet)
t.crawl(only_english=True)

#Index all the documents
docs = ws.get_documents_by_date(from_date, to_date, type=SudanTweet)
index = Index(index_path)
print 'Started indexing'
index.add_documents(docs)
index.finalize()
print 'Started indexing'
for term in index.get_top_terms(limit=100):
    print term