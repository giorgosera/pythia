'''
Created on 26 Jan 2012

@author: george
'''
import unittest
import numpy
from analysis.clustering.datastructures.clusters import CustomClusterer
from analysis.clustering.algorithms.algorithms import hierarchical, kmeans, cosine, tanimoto


###########################################
# GLOBALS                                #
###########################################
doc1 = 'frequent FrEquEnt frequent <li>word</li> word sentence sentence' 
doc2 = 'sentence <a href="www.google.com">arab</a> spring'
doc3 = 'a is not a toKENIzed document'
samples = [doc1, doc2, doc3] 

cc = CustomClusterer()        
i = 0
for sample in samples:
    cc.add_document(i, sample)
    i += 1
cc.construct_term_doc_matrix()

class Test(unittest.TestCase):

    def test_cluster_term_document_matrix(self):

        calculated = cc.td_matrix
        expected = numpy.array([[ 0.31388923,  0.11584717,  0,           0,           0,           0,           0.47083384], 
                                [ 0,           0.13515504,  0.3662041,   0,           0.3662041,   0,           0         ],      
                                [ 0,           0,           0,           0.54930614,  0,           0.549306140, 0        ]])
        
        self.assertEqual(expected.all(), calculated.all())
        
    def test_save_matrix_to_file(self):
        cc.save_table("sample_table_custom")
        
    def test_load_table_from_file(self):
        cc.save_table("sample_table_custom")
        rownames, colnames, data = cc.load_table()
        expected_rownames = ['0', '1', '2'] 
        expected_colnames = ['word', 'sentenc', 'arab', 'token', 'spring', 'document', 'frequent'] 
        expected_data = [[0.313889, 0.115847, 0.0, 0.0, 0.0, 0.0, 0.470834], 
                         [0.0, 0.135155, 0.366204, 0.0, 0.366204, 0.0, 0.0], 
                         [0.0, 0.0, 0.0, 0.549306, 0.0, 0.549306, 0.0]]

        self.assertEqual(expected_rownames, rownames)
        self.assertEqual(expected_colnames, colnames)
        self.assertEqual(expected_data, data)
        
    def test_matrix_rotation(self):
        rtd = cc.rotate_td_matrix()
        expected = [[0.31388922533374564, 0.0, 0.0], 
                    [0.11584717374518982, 0.13515503603605478, 0.0], 
                    [0.0, 0.36620409622270322, 0.0], 
                    [0.0, 0.0, 0.54930614433405489], 
                    [0.0, 0.36620409622270322, 0.0], 
                    [0.0, 0.0, 0.54930614433405489], 
                    [0.47083383800061845, 0.0, 0.0]]
        
        self.assertEqual(expected, rtd)
    
    def test_split_into_clusters(self):
        cc.construct_term_doc_matrix()
        cc.save_table("orange_clustering_test")
        k = 2
        rownames, colnames, data = cc.load_table()
        km = kmeans(data=data, similarity=cosine, k=2)

        cc.split_documents(km, k)
    
        expected_clusters = [{'0': {'tokens': ['frequent', 'frequent', 'frequent', 'word', 'word', 'sentenc', 'sentenc'], 'raw': 'frequent FrEquEnt frequent <li>word</li> word sentence sentence', 'word_frequencies': [('frequent', 3), ('sentenc', 2), ('word', 2)]}, '2': {'tokens': ['token', 'document'], 'raw': 'a is not a toKENIzed document', 'word_frequencies': [('document', 1), ('token', 1)]}}
                             ,{'1': {'tokens': ['sentenc', 'arab', 'spring'], 'raw': 'sentence <a href="www.google.com">arab</a> spring', 'word_frequencies': [('arab', 1), ('sentenc', 1), ('spring', 1)]}}]
         
        self.assertEqual(expected_clusters, [c.get_documents() for c in cc.clusters])
        
        cc.dump_clusters_to_file("test_cluster_with_samples")

        #The dump should read like below.
        #=======================================================================
        # ***********************************************************
        # Cluster0
        # Most frequent terms:('frequent', 3)('sentenc', 2)('word', 2)('document', 1)('token', 1)
        # frequent FrEquEnt frequent <li>word</li> word sentence sentence
        # a is not a toKENIzed document
        # 
        # ***********************************************************
        # Cluster1
        # Most frequent terms:('arab', 1)('sentenc', 1)('spring', 1)
        # sentence <a href="www.google.com">arab</a> spring
        #=======================================================================

if __name__ == "__main__":
    unittest.main()