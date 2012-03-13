'''
Created on 26 Jan 2012

@author: george
'''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

####################################### <---- WARNING ----> ##################################################
THESE TESTS NO LONGER WORK SINCE NOW WE CRAWL THE STATS INSTEAD OF CALCULATING THEM FROM THE DATASET. HOWEVER, WE KEEP ALL THE 
FUNCTION IN DEPRECATED/SCRAPY. IN FUTURE IF WE NEED TO CALCULATE USERS STATS WE CAN REUSE THEM.

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
        TestAuthor.drop_collection()
        a = TestAuthor()
        a.screen_name = "ianinegypt"
        a.tweets = docs1
        a.calculate_author_stats()
        expected = [7, 2, 569, 2, 1]
        calculated = [a.retweets, a.links, a.retweeted_tweets, a.replies_to_others, a.mentions_to_others]
        self.assertEqual(expected, calculated)
        TestAuthor.drop_collection()
        
    def test_author_stats_multiple_authors(self):
        TestAuthor.drop_collection()
        a1 = TestAuthor()
        a1.screen_name = "ianinegypt1"
        a1.tweets = [docs2[0], docs2[1], docs2[2]]
        a1.save()
        
        a2 = TestAuthor()
        a2.screen_name = "ianinegypt2"
        a2.tweets = [docs2[3]]
        a2.save()

        a1.calculate_author_stats()
        calculated1 = [a1.retweets, a1.links, a1.retweeted_tweets, a1.replies_to_others, a1.mentions_to_others]
        a2.calculate_author_stats()
        calculated2 = [a2.retweets, a2.links, a2.retweeted_tweets, a2.replies_to_others, a2.mentions_to_others]
        
        expected1 = [1, 2, 20, 0, 2]
        expected2 = [0, 1, 16, 1, 0]
        self.assertEqual(expected1, calculated1)
        self.assertEqual(expected2, calculated2)
        TestAuthor.drop_collection()
        
    def test_feature_vector_construction(self):
        TestAuthor.drop_collection()
        a = TestAuthor()
        a.screen_name = "ianinegypt"
        a.tweets = docs1
        a.followers_count = 100
        a.friends_count = 4
        fv = a.update_feature_vector()
        expected = [0.17948718, 0.05128205, 0.0685413, 0.0512820512, 0.02564102564, 25.] 
        self.assertAlmostEqual(numpy.sum(numpy.array(expected) - numpy.array(fv)), 0)
        TestAuthor.drop_collection()
        
    def test_feature_vector_construction_after_update(self):
        TestAuthor.drop_collection()
        a = TestAuthor()
        a.screen_name = "ianinegypt"
        a.tweets = docs1
        a.followers_count = 100
        a.friends_count = 4
        fv = a.update_feature_vector()
        expected = [0.17948718, 0.05128205, 0.0685413, 0.0512820512, 0.02564102564, 25.] 
        self.assertAlmostEqual(numpy.sum(numpy.array(expected) - numpy.array(fv)), 0)
        
        #Then append some new docs
        a.tweets.extend(docs2)
        fv = a.update_feature_vector()
        expected = [0.18604651162790697, 0.11627906976744186, 0.07557117750439367, 0.06976744186046512, 0.06976744186046512, 25.0]
        self.assertAlmostEqual(numpy.sum(numpy.array(expected) - numpy.array(fv)), 0)
        
        TestAuthor.drop_collection()
        
if __name__ == "__main__":
    unittest.main()