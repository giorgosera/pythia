'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import unittest
from analysis.text import TextAnalyser
from analysis.clustering.algorithms.algorithms import hierarchical, cosine

class TestHierarchicalClustering(unittest.TestCase):
    
    def test_hierarchical(self):
        #=======================================================================
        # doc0 = 'This is a document related to sports : Football, basketball, tennis etc.' 
        # doc1 = 'In this document we will be talking about basketball, football, tennis and sports in general.'
        # doc2 = 'Football is an amazing sport. I love it. But I love basketball too and tennis'
        # doc3 = 'This document is related to programming. More specifically Python and C++'
        # doc4 = 'I wrote a small Python script to run a clustering algorithm'
        # doc5 = 'This blog writes about Python and programming in general.'
        #=======================================================================
        
        doc0 = 'Hello Hello Hello Hello Hello Hello '
        doc1 = 'Hello Hello Hello Hello Hello Hello '
        doc2 = 'Hello Hello Hello Hello Hello Hello ' 
        doc3 = 'Bye Bye Bye Bye Bye '
        doc4 = 'Bye Bye Bye Bye Bye '
        doc5 = 'Bye Bye Bye Bye Bye ' 
    
        sample_docs = [doc0, doc1, doc2, doc3, doc4, doc5]

        analyser = TextAnalyser()
        for s in sample_docs:
            analyser.add_document(s)
                 
        analyser.save_frequency_matrix("test.txt")
        rownames, colnames, data = analyser.read_frequency_matrix("test.txt")

        cluster = hierarchical(data, cosine)
        cluster.print_it(rownames)
        
        
if __name__ == "__main__":
    unittest.main()