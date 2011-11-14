'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis package.
'''
import unittest
from analysis.text import TextAnalyser

class TestTextAnalyserFunctions(unittest.TestCase):
    
    def test_frequency_distribution(self):
    
        sample_tweets = ['frequent frequent frequent frequent frequent word word sentence sentence', 
                         'sentence arab spring'
                        ]
        
        expected = ['frequent', 'sentence', 'word', 'arab', 'spring']
        
        analyser = TextAnalyser(sample_tweets)
        estimated = analyser.frequency_distribution()

        self.assertEqual(expected, estimated.keys())
    
    def test_retweet_patterns(self):
        sample_tweets = [
                         'RT @GeorgeEracleous Viva la revolucion',
                         'RT @GeorgeEracleous Python is amazing', 
                         'Coding at 0100 in the night is not healthy man (via @ChuckNorris'
                         ] 
        
        expected = [
                    ('RT', ' @GeorgeEracleous'), 
                    ('RT', ' @GeorgeEracleous'), 
                    ('via', ' @ChuckNorris')
                   ]
        
        analyser = TextAnalyser(sample_tweets)
        estimated = analyser.retweets_patterns()
        
        self.assertEqual(expected, estimated)
        
        
if __name__ == "__main__":
    unittest.main()