'''
Created on 26 Jan 2012

@author: george
'''
import unittest
from analysis.clustering.structures import Cluster
from tests.test_document import get_orange_clustering_test_data

###########################################
# GLOBALS                                #
###########################################
samples  =  get_orange_clustering_test_data()
doc_dict = {}
id = 0
for sample in samples:
    doc_dict[id] = sample.content
    id += 1

c = Cluster(id=1, document_dict=doc_dict)        

class Test(unittest.TestCase):

    def test_cluster_term_document_matrix(self):
        sentiment = c.get_sentiment(cumulative=False)
        print sentiment

if __name__ == "__main__":
    unittest.main()