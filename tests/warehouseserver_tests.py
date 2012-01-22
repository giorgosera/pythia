'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import unittest
from database.getters import WarehouseServer
from analysis.text import TextAnalyser
from analysis.clustering.algorithms.algorithms import hierarchical, cosine, pearson
from visualizations.dendrogram import Dendrogram

class TestWarehouseServer(unittest.TestCase):
    
    def test_text_clustering(self):        
        ws = WarehouseServer()
        items = ws.get_documents_by_date(1, 2)
        
        t = TextAnalyser()
        for i in items:
            t.add_document(i.text)
        
        t.save_frequency_matrix("tweet_clusters.txt")
        rownames, colnames, data = t.read_frequency_matrix("tweet_clusters.txt")
        data = t.rotate_frequency_matrix()
        cluster = hierarchical(data, similarity=pearson)
        
        dendro = Dendrogram(cluster, colnames, "tweet_cluster.jpg", cluster.get_height(), cluster.get_depth())
        dendro.draw_node(10, cluster.get_height()/2)
            
        
if __name__ == "__main__":
    unittest.main()