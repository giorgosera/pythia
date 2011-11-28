'''
Created on 27 Nov 2011

@author: george
'''
import unittest
from crawlers.CrawlerFactory import CrawlerFactory

class TestGraphFunctions(unittest.TestCase):
    
    def test_construction_of_twitter_crawlers(self):
        factory = CrawlerFactory()
        t = factory.get_crawler("twitter")
        t.login()
        info = t.getUserInfoByScreenName("GeorgeEracleous")
        
if __name__ == "__main__":
    unittest.main()