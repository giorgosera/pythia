'''
Created on 1 Feb 2012

@author: george
'''
import unittest, nltk
from analysis.semantic import TwitterSemanticAnalyser

tweet1 = "RT @monaeltahawy: RT @Gheblawi Beyond belief: religious history &amp; make-up of #Egypt interesting discussion #Copts http://www.bbc.co.uk/podcasts/series/belief"
tweet2 = "Breaking News - Messi spotted outside the Etihad #transferdeadlineday http://twitpic.com/8dwcum (via @AndrewBloch )"
tweet3 = "This is not a retweet #test"
tweet4 = "RT Beyond belief: religious history &amp; make-up of #Egypt interesting discussion #Copts http://www.bbc.co.uk/podcasts/series/belief"
tweet5 = "This is Egypt. Hello my name is Bob Jones.  I am speaking to you at this very moment.  Are you listening to me, Bob?"
tweet6 = "This is so sad. I am desperate"
tweet7 = "I am so happy!"
corpus = [tweet1, tweet2, tweet3, tweet4, tweet5, tweet6, tweet7]
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
        self.assertEqual(('negative', '-0.200008'), calculated_sad)
        self.assertEqual(('positive', '0.61373'), calculated_happy)
       
    def test_extract_keywords(self):
        tsa = TwitterSemanticAnalyser()
        calculated = tsa.extract_keywords(tweet5)
        expected = ['Bob Jones', 'Egypt']
        self.assertEqual(expected, calculated) 
       
    def test_analysing_multiple_docs(self):
        tsa = TwitterSemanticAnalyser()
        calculated = tsa.analyse_corpus(corpus)
        expected = [([], ('positive', '0.0593345'), ['Gheblawi Beyond belief', 'Egypt interesting discussion', 'religious history', 'make-up', 'interesting']), ([], ('negative', '-0.31492'), ['Messi', 'News']), ([('retweet', 'FieldTerminology')], ('neutral', 0), []), ([], ('positive', '0.060677'), ['RT Beyond belief', 'Egypt interesting discussion', 'religious history', 'make-up', 'interesting']), ([('Bob Jones', 'Person'), ('Bob', 'Person'), ('Egypt', 'Country')], ('neutral', 0), ['Bob Jones', 'Egypt']), ([], ('negative', '-0.200008'), []), ([], ('positive', '0.61373'), ['happy'])]
        self.assertEquals(expected, calculated)

         
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRetweetCounter']
    unittest.main()