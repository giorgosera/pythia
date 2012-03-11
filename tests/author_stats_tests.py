'''
Created on 26 Jan 2012

@author: george
'''
import unittest, numpy
from tests.test_document import get_single_author_initialisation_data, get_multiple_author_initialisation_data
from database.model.agents import TestAuthor
###########################################
# GLOBALS                                #
###########################################
docs1 =  get_single_author_initialisation_data()
docs2 =  get_multiple_author_initialisation_data()

class Test(unittest.TestCase):

    def test_author_stats_single_author(self):
        a = TestAuthor()
        a.screen_name = "ianinegypt"
        a.tweets = docs1
        a.calculate_author_stats()
        expected = [7, 2, 569, 1, 0]
        calculated = [a.retweets, a.links, a.retweeted_tweets, a.replies_to_others, a.mentions_by_others]
        self.assertEqual(expected, calculated)
        TestAuthor.drop_collection()
        
    def test_author_stats_multiple_authors(self):
        a1 = TestAuthor()
        a1.screen_name = "ianinegypt1"
        a1.tweets = [docs2[0], docs2[1], docs2[2]]
        a1.save()
        
        a2 = TestAuthor()
        a2.screen_name = "ianinegypt2"
        a2.tweets = [docs2[3]]
        a2.save()

        a1.calculate_author_stats()
        calculated1 = [a1.retweets, a1.links, a1.retweeted_tweets, a1.replies_to_others, a1.mentions_by_others]
        a2.calculate_author_stats()
        calculated2 = [a2.retweets, a2.links, a2.retweeted_tweets, a2.replies_to_others, a2.mentions_by_others]
        
        expected1 = [1, 2, 20, 2, 0]
        expected2 = [0, 1, 16, 1, 0]
        self.assertEqual(expected1, calculated1)
        self.assertEqual(expected2, calculated2)
        
    def test_feature_vector_construction(self):
        a = TestAuthor()
        a.screen_name = "ianinegypt"
        a.tweets = docs1
        a.followers_count = 100
        a.friends_count = 4
        fv = a.get_feature_vector()
        expected = [0.17948718, 0.05128205, 0.0685413, 0.02564103, 0., 25.] 
        self.assertAlmostEqual(numpy.sum(expected - fv), 0)
        
if __name__ == "__main__":
    unittest.main()