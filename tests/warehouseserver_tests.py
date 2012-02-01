'''
Created on 13 Nov 2011

@author: george

Unit tests for the database.getters package.
'''
import unittest

from database.warehouse import WarehouseServer
from analysis.text import TextAnalyser
from analysis.clustering.algorithms import *
from visualizations.dendrogram import Dendrogram
from visualizations.Cluster2DPlot import Cluster2DPlot

##############################
# GLOBALS                    #
##############################
ws = WarehouseServer()

class TestWarehouseServer(unittest.TestCase):
    
    def test_getters(self):
        n = 10
        items = ws.get_n_documents(n)
        self.assertEqual(n, len(items))
        
if __name__ == "__main__":
    unittest.main()