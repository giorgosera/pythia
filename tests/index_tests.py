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

class TestPlayground(unittest.TestCase):
  
    def test_indexing(self):
        index = Index("index")
        for doc in sample_docs:
            index.add_document(doc)
        index.finalize()
        results = index.search("sales")
        
        calculated = []
        for doc in results:
            calculated.append(doc.get('id'))
            
        expected = ['4f2d602780286c38a7000013', '4f2d603280286c38a700001e']

        self.assertEqual(expected, calculated)
        
if __name__ == "__main__":
    unittest.main()




