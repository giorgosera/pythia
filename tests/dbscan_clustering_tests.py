'''
Created on 26 Jan 2012

@author: george
'''
import unittest, datetime
from analysis.clustering.dbscan import DBSCANClusterer
from database.warehouse import WarehouseServer

###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()
    
class Test_Dbscan_clustering(unittest.TestCase):

    def test_dbscan_clustering_with_tweets(self):
        from_date = datetime.datetime(2011, 1, 23, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 27, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, limit=1000)
        
        epsilon = 0.2
        min_pts = 1.0
        #=======================================================================
        # points = []
        # points.append([1,1])
        # points.append([1.5,1])
        # points.append([1.8,1.5])
        # points.append([2.1,1])
        # points.append([3.1,2])
        # points.append([4.1,2])
        # points.append([5.1,2])
        # points.append([10,10])
        # points.append([11,10.5])
        # points.append([9.5,11])
        # points.append([9.9,11.4])
        # points.append([15.0, 17.0])
        # points.append([15.0, 17.0])
        # points.append([7.5, -5.0])
        #=======================================================================
        dbscan = DBSCANClusterer()
        dbscan.add_documents(items)
        clusters = dbscan.run(epsilon, min_pts, pca=True)
        print '\n========== Results of Clustering ============='
        for cluster, members in clusters.iteritems():
            print '\n--------Cluster %d---------' % cluster
            for point in members:
                print point
        
        print clusters.keys()
        
        #expected = {0: [[1, 1], [1.5, 1], [1.8, 1.5], [2.1, 1], [1, 1], [3.1, 2], [4.1, 2], [5.1, 2]], 1: [[10, 10], [11, 10.5], [9.5, 11], [9.9, 11.4]], -1: [[15.0, 17.0], [15.0, 17.0], [7.5, -5.0]]}
        #self.assertEqual(expected, clusters)
    
if __name__ == "__main__":
    unittest.main()