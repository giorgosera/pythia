# -*- coding: utf-8 -*-
'''
Created on 23 Jan 2012

@author: george

My playground!
'''
import unittest
from visualizations.graphs import Timeline  
from database.warehouse import WarehouseServer
from database.model.tweets import EgyptTweet

ws = WarehouseServer()

class TestPlayground(unittest.TestCase):
    
    def test_timeline(self):
        items = [item.date for item in ws.get_all_documents(type=EgyptTweet)]
        t = Timeline(items)
        t.plot()
        t.show()

if __name__ == "__main__":
    unittest.main()