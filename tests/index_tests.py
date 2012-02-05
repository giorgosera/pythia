# -*- coding: utf-8 -*-
'''
Created on 23 Jan 2012

@author: george

My playground!
'''
import unittest
from analysis.index import Index
from database.warehouse import WarehouseServer
from database.model.tweets import TwoGroupsTweet

ws = WarehouseServer()
sample_docs = ws.get_n_documents(100, type=TwoGroupsTweet)

index = Index("index")
for doc in sample_docs:
    index.add_document(doc)
index.finalize()

class TestPlayground(unittest.TestCase):
  
    def test_searching(self):        
        results = index.search("sales")
        
        calculated = []
        for doc in results:
            calculated.append(doc.get('id'))
            
        expected = ['4f2d602780286c38a7000013', '4f2d603280286c38a700001e']

        self.assertEqual(expected, calculated)
    
    def test_top_terms_index(self):
        results = index.get_top_keywords(10)
        expected = [(52, u'uk'), (8, u'us'), (8, u'new'), (6, u'week'), (5, u'last'), (5, u'host'), (4, u'yeah'), (4, u'want'), (4, u'presid'), (4, u'nation')]
        self.assertEquals(expected, results)
        
    

if __name__ == "__main__":
    unittest.main()




