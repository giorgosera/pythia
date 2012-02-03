'''
Created on 13 Nov 2011

@author: george

Unit tests for the database.getters package.
'''
import unittest, datetime
from database.warehouse import WarehouseServer
from database.model.tweets import *

##############################
# GLOBALS                    #
##############################
ws = WarehouseServer()

class TestWarehouseServer(unittest.TestCase):
    
    def test_getters(self):
        n = 10
        items = ws.get_n_documents(n)
        self.assertEqual(n, len(items))
        
    def test_get_top_by_date(self):

        tweet1 = EgyptTweet()
        tweet1.date = datetime.datetime(2015, 01, 27, 0, 0, 0)
        tweet1.retweet_count = 10
        tweet1.content = {'test': "test_tweet1"}
        tweet1.screen_name ="test_tweet"
        tweet1.url ="test_url"
        tweet1.author_name ="test_name"
        tweet1.author_screen_name ="test_name"
        tweet2 = EgyptTweet()
        tweet2.date = datetime.datetime(2015, 01, 27, 0, 0, 0)
        tweet2.retweet_count = 5
        tweet2.screen_name ="test_tweet"
        tweet2.url ="test_url"
        tweet2.content = {'test': "test_tweet2"}
        tweet2.author_name ="test_name"
        tweet2.author_screen_name ="test_name"
        tweet1.save()
        tweet2.save()
        
        from_date = datetime.datetime(2014, 01, 27, 0, 0, 0)
        to_date = datetime.datetime(2015, 01, 28, 0, 0, 0)
        
        result = []
        for item in ws.get_top_documents_by_date(from_date, to_date, threshold=7):
            result.append(item.content)
            
        self.assertEquals({'test': "test_tweet1"}, result[0])
        
        #Erases the two test tweets
        for item in EgyptTweet.objects(date = datetime.datetime(2015, 01, 27, 0, 0, 0)):
            item.delete()
            
        
if __name__ == "__main__":
    unittest.main()