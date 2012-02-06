'''
Created on 1 Feb 2012

@author: george
'''
import unittest
from analysis.social import TwitterSocialAnalyser
from analysis.text import TextAnalyser
from collections import OrderedDict

tweet_with_RT = "RT @monaeltahawy: RT @Gheblawi Beyond belief: religious history &amp; make-up of #Egypt interesting discussion #Copts http://www.bbc.co.uk/podcasts/series/belief"
tweet_with_VIA= "Breaking News - Messi spotted outside the Etihad #transferdeadlineday http://twitpic.com/8dwcum (via @AndrewBloch )"
not_a_retweet = "This is not a retweet #test"
tweet_with_almost_RT = "RT Beyond belief: religious history &amp; make-up of #Egypt interesting discussion #Copts http://www.bbc.co.uk/podcasts/series/belief"
tweets = [tweet_with_RT, tweet_with_VIA, not_a_retweet, tweet_with_almost_RT]

t = TextAnalyser()
dataset = OrderedDict()
id = 0
for tweet in tweets:
    d = t.add_document(tweet)
    dataset[id] = d
    id += 1
    
class Test(unittest.TestCase):
    def test_retweet_filter(self):
        tsa = TwitterSocialAnalyser(dataset)
        result = tsa.filter_retweets()
        expected = []
        expected.append( (0, t.add_document(tweet_with_RT)) )
        expected.append( (1, t.add_document(tweet_with_VIA)) )
        self.assertEqual(result, OrderedDict(expected))

        
    def test_mention_filter(self):
        pass
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRetweetCounter']
    unittest.main()