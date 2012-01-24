'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import unittest

import Orange  #!@UnresolvedImport
from Orange.clustering import hierarchical  #!@UnresolvedImport

class TestHierarchicalClustering(unittest.TestCase):
    
    def test_hierarchical(self): 
        def printClustering(cluster):
            if cluster.branches:
                return "(%s%s)" % (printClustering(cluster.left), printClustering(cluster.right))
            else:
                return str(cluster[0])       
        m = [[],
             [ 3],
             [ 2, 4],
             [17, 5, 4],
             [ 2, 8, 3, 8],
             [ 7, 5, 10, 11, 2],
             [ 8, 4, 1, 5, 11, 13],
             [ 4, 7, 12, 8, 10, 1, 5],
             [13, 9, 14, 15, 7, 8, 4, 6],
             [12, 10, 11, 15, 2, 5, 7, 3, 1]]
        matrix = Orange.core.SymMatrix(m)
        root = hierarchical.HierarchicalClustering(matrix,
                linkage=hierarchical.HierarchicalClustering.Average)
        print printClustering(root)
        
if __name__ == "__main__":
    unittest.main()