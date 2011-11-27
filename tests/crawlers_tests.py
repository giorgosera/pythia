'''
Created on 27 Nov 2011

@author: george
'''
import unittest
from crawlers.CrawlerFactory import CrawlerFactory
from crawlers.TwitterCrawler import TwitterCrawler

class TestGraphFunctions(unittest.TestCase):
    
    def test_construction_of_twitter_crawlers(self):
        factory = CrawlerFactory()
        t = factory.get_crawler("twitter")
        t = t.login()
        

if __name__ == "__main__":
    unittest.main()