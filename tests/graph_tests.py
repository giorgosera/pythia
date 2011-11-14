'''
Created on 14 Nov 2011

@author: george

Unit tests for the graph package
'''
import unittest
from analysis.graph import RetweetGraphBuilder

class TestGraphFunctions(unittest.TestCase):
    
    def test_construction_of_retweet_graph(self):
        sample_tweets = [
                         {'id':1, 'text':'RT @GeorgeEracleous Viva la revolucion', 'from_user':'@ChuckNorris'},
                         {'id':2, 'text':'RT @GeorgeEracleous Python is amazing', 'from_user':'@ChuckNorris'}, 
                         {'id':3, 'text':'Coding at 0100 in the night is not healthy man (via @ChuckNorris', 'from_user':'@GeorgeEracleous'}
                         ] 
        gbuilder = RetweetGraphBuilder(sample_tweets)
        gbuilder.construct_graph_from_retweets()
        graph = gbuilder.get_graph()
        
        self.assertEqual(2, graph.number_of_nodes())
        self.assertEqual(2, graph.number_of_edges()) 
        
        
if __name__ == "__main__":
    unittest.main()