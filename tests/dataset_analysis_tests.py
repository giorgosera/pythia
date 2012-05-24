# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the DatasetAnalyser class.
'''
import unittest
from analysis.dataset_analysis import DatasetAnalyser
from tests.test_document import get_test_documents 

e,r,docs = get_test_documents()

class TestToolsFunctions(unittest.TestCase):
    
    def test_avg_document_length(self):
        da = DatasetAnalyser(docs)
        calculated = da.avg_document_length()
        self.assertEqual(47, calculated)
        
    def test_vocabulary_size(self):
        da = DatasetAnalyser(docs)
        calculated = da.vocabulary_size()
        self.assertEqual(7, calculated)

    def test_avg_vocabulary_size(self):
        da = DatasetAnalyser(docs)
        calculated = da.avg_vocabulary_size()
        self.assertAlmostEqual(2.33, calculated, places=2)
        
if __name__ == "__main__":
    unittest.main()