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
    
#    def test_entity_extraction(self):
#        tsa = TwitterSemanticAnalyser()
#        calculated = tsa.extract_entities(tweet5)
#        expected = [('Bob Jones', 'Person'), ('Bob', 'Person'), ('Egypt', 'Country')]
#        self.assertEqual(expected, calculated)
#       
#    def test_sentiment_extraction(self):
#        tsa = TwitterSemanticAnalyser()
#        calculated_sad = tsa.extract_sentiment(tweet6)
#        calculated_happy = tsa.extract_sentiment(tweet7)
#        self.assertEqual("negative", calculated_sad)
#        self.assertEqual("positive", calculated_happy)
#       
#    def test_extract_keywords(self):
#        tsa = TwitterSemanticAnalyser()
#        calculated = tsa.extract_keywords(tweet5)
#        expected = ['Bob Jones', 'Egypt']
#        self.assertEqual(expected, calculated) 
#       
#    def test_analysing_multiple_docs(self):
#        tsa = TwitterSemanticAnalyser()
#        calculated = tsa.analyse_corpus(corpus)
#        expected = [([], 'positive', ['Gheblawi Beyond belief', 'Egypt interesting discussion', 'religious history', 'make-up', 'interesting']), ([], 'negative', ['Messi', 'News']), ([('retweet', 'FieldTerminology')], 'neutral', []), ([], 'positive', ['RT Beyond belief', 'Egypt interesting discussion', 'religious history', 'make-up', 'interesting']), ([('Bob Jones', 'Person'), ('Bob', 'Person'), ('Egypt', 'Country')], 'neutral', ['Bob Jones', 'Egypt']), ([], 'negative', []), ([], 'positive', ['happy'])]
#        self.assertEquals(expected, calculated)
    
    def test_kati(self):
        tokens = nltk.pos_tag(nltk.WordPunctTokenizer().tokenize(tweet1))
        for p in nltk.ne_chunk(tokens):
            print p
         
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRetweetCounter']
    unittest.main()