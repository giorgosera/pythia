'''
Created on 26 Jan 2012

@author: george
'''
import unittest
from analysis.clustering.datastructures.clusters import CustomCluster
from analysis.text import TextAnalyser
import numpy

###########################################
# GLOBALS                                #
###########################################
doc1 = 'frequent FrEquEnt frequent <li>word</li> word sentence sentence' 
doc2 = 'sentence <a href="www.google.com">arab</a> spring'
doc3 = 'a is not a toKENIzed document'
samples = [doc1, doc2, doc3] 

ta = TextAnalyser()
cc = CustomCluster()        
i = 0
for sample in samples:
    index, d = ta.add_document(i, sample)
    cc.add_document(index, d)
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

        

if __name__ == "__main__":
    unittest.main()