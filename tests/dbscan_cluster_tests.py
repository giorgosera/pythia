'''
Created on 26 Jan 2012

@author: george
'''
import unittest, datetime
from analysis.clustering.dbscan import DBSCANClusterer
from database.warehouse import WarehouseServer
from collections import OrderedDict

###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()
epsilon = 2.0
min_pts = 2.0
points = []
points.append([1,1])
points.append([1.5,1])
points.append([1.8,1.5])
points.append([2.1,1])
points.append([3.1,2])
points.append([4.1,2])
points.append([5.1,2])
points.append([10,10])
points.append([11,10.5])
points.append([9.5,11])
points.append([9.9,11.4])
points.append([15.0, 17.0])
points.append([15.0, 17.0])
points.append([7.5, -5.0])
dbscan = DBSCANClusterer()
#Small hacks..in normal usage never set td_matrix by urself 
#and never populate a dummy document_dict
dbscan.td_matrix = points  
dbscan.document_dict = OrderedDict( [('0','dummy'), ('1', 'dummy'), ('2', 'dummy'),('3', 'dummy'),('4', 'dummy'),('5', 'dummy'),
                        ('6', 'dummy'),('7', 'dummy'),('8', 'dummy'),('9', 'dummy'),('10', 'dummy'),('11', 'dummy'),('12', 'dummy'),('13', 'dummy')])
  
class Test_Dbscan_clustering(unittest.TestCase):

    def test_dbscan_cluster(self):
        clusters = dbscan.run(epsilon, min_pts)
        print '\n========== Results of Clustering ============='
        for cluster, members in clusters.iteritems():
            print '\n--------Cluster %d---------' % cluster
            for point in members:
                print point
        
        expected = {0: [('0', [1, 1]), ('1', [1.5, 1]), ('2', [1.8, 1.5]), ('3', [2.1, 1]), ('0', [1, 1]), ('4', [3.1, 2]), ('5', [4.1, 2]), ('6', [5.1, 2])], 
                    1: [('7', [10, 10]), ('8', [11, 10.5]), ('9', [9.5, 11]), ('10', [9.9, 11.4])], 
                    -1: [('11', [15.0, 17.0]), ('12', [15.0, 17.0]), ('13', [7.5, -5.0])]}
        self.assertEqual(expected, clusters)

    def test_split_documents(self):
        clusters = dbscan.run(epsilon, min_pts)
        expected = [OrderedDict([('0', 'dummy'), ('1', 'dummy'), ('2', 'dummy'), ('3', 'dummy'), ('4', 'dummy'), ('5', 'dummy'), ('6', 'dummy')]), OrderedDict([('7', 'dummy'), ('8', 'dummy'), ('9', 'dummy'), ('10', 'dummy')]), OrderedDict([('11', 'dummy'), ('12', 'dummy'), ('13', 'dummy')])]
        self.assertEqual(expected, [cluster.document_dict for cluster in dbscan.clusters])
    
if __name__ == "__main__":
    unittest.main()