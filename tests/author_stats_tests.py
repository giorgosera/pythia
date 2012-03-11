'''
Created on 26 Jan 2012

@author: george
'''
import unittest
from tests.test_document import get_author_initialisation_data
from database.model.agents import TestAuthor
###########################################
# GLOBALS                                #
###########################################
docs  =  get_author_initialisation_data()

class Test(unittest.TestCase):

    def test_author_stats_single_author(self):
        a = TestAuthor()
        a.screen_name = "ianinegypt"
        a.tweets = docs
        a.calculate_author_stats()
        print a.retweets
        print a.links
        print a.retweeted_tweets
        print a.replies_to_others
        print a.mentions_by_others

if __name__ == "__main__":
    unittest.main()