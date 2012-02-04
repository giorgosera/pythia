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
        index.search("critic")
        
if __name__ == "__main__":
    unittest.main()

#4f2c3d6880286c53bf000001


