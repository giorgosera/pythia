'''
Created on 1 Feb 2012

@author: george
'''
import unittest
from analysis.semantic import TwitterSemanticAnalyser

tweet1 = "RT @monaeltahawy: RT @Gheblawi Beyond belief: religious history &amp; make-up of #Egypt interesting discussion #Copts http://www.bbc.co.uk/podcasts/series/belief"
tweet2 = "Breaking News - Messi spotted outside the Etihad #transferdeadlineday http://twitpic.com/8dwcum (via @AndrewBloch )"
tweet3 = "This is not a retweet #test"
tweet4 = "RT Beyond belief: religious history &amp; make-up of #Egypt interesting discussion #Copts http://www.bbc.co.uk/podcasts/series/belief"
tweet5 = "This is Egypt. Hello my name is Bob Jones.  I am speaking to you at this very moment.  Are you listening to me, Bob?"
tweet6 = "This is so sad. I am desperate"
tweet7 = "I am so happy!"

class Test(unittest.TestCase):
    
    def test_entity_extraction(self):
        tsa = TwitterSemanticAnalyser()
        calculated = tsa.extract_entities(tweet5)
        expected = [('Bob Jones', 'Person'), ('Bob', 'Person'), ('Egypt', 'Country')]
        self.assertEqual(expected, calculated)
        
    def test_sentiment_extraction(self):
        tsa = TwitterSemanticAnalyser()
        calculated_sad = tsa.extract_sentiment(tweet6)
        calculated_happy = tsa.extract_sentiment(tweet7)
        self.assertEqual("negative", calculated_sad)
        self.assertEqual("positive", calculated_happy)
        
    def test_extract_keywords(self):
        tsa = TwitterSemanticAnalyser()
        calculated = tsa.extract_keywords(tweet5)
        expected = ['Bob Jones', 'Egypt']
        self.assertEqual(expected, calculated) 
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRetweetCounter']
    unittest.main()