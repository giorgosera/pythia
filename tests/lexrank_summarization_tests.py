'''
Created on 27 Nov 2011

@author: george
'''
import unittest, numpy
from analysis.summarization.summarization import LexRankSummarizer
from tests.test_document import get_orange_clustering_test_data

test_documents = get_orange_clustering_test_data()
doc_dict = {}
id = 0
for doc in test_documents:
    doc_dict[id] = doc.content
    id +=1
    
class TestLexRankSummarizationFunctions(unittest.TestCase):
    
    def test_cosine_matrix_creation(self): 
        lrs = LexRankSummarizer(doc_dict)
        res=lrs.summarize(threshold=0.1, tolerance=0.0001)
        print res
        
if __name__ == "__main__":
    unittest.main()