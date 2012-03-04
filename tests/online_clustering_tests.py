'''
Created on 26 Jan 2012

@author: george
'''
import unittest, datetime
from analysis.clustering.online import OnlineClusterer
from database.warehouse import WarehouseServer
import pylab#!@UnresolvedImport
###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()
    
class Test_online_clustering(unittest.TestCase):

    def test_online_clustering_with_tweets(self):
        from_date = datetime.datetime(2011, 1, 25, 12, 0, 0)
        to_date = datetime.datetime(2011, 1, 26, 12, 30, 0) 
        items = ws.get_documents_by_date(from_date, to_date, limit=100)             
        
        window = 20
        oc = OnlineClusterer(N=20, window = window)
        for item in items:
            index = oc.add_document(item)
            oc.cluster(index, str(item.id), item.content)
            if index >= window:
                pylab.scatter(oc.td_matrix[window-2][0], oc.td_matrix[window-2][1])
            elif index > 0:
                pylab.scatter(oc.td_matrix[index][0], oc.td_matrix[index][1])

        clusters=oc.trimclusters()            
        oc.dump_clusters_to_file("online_with_tweets")
        #oc.plot_scatter()

        for cluster in oc.clusters:
            print cluster.id
            print cluster.get_size()
            print '-----------------'

        cx=[x.center[0] for x in oc.clusters]
        cy=[y.center[1] for y in oc.clusters]
    
        pylab.plot(cx,cy,"ro")
        pylab.draw()
        pylab.show()
         
if __name__ == "__main__":
    unittest.main()