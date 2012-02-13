'''
Created on 8 Feb 2012

@author: george
'''
from math import pow, sqrt
from analysis.clustering.algorithms import euclidean
from analysis.clustering.abstract import AbstractClusterer
from analysis.clustering.structures import Cluster
from collections import OrderedDict

class DBSCANClusterer(AbstractClusterer):
    '''
    A simple implementation of the DBSCAN density based clustering a
    algorithm. 
    ACKNOWLEDGMENT: The code is adapted from https://github.com/jessykate/DBScan
                    which provides a robust implementation of the algorithm.
    '''        
    def _as_points(self, points):
        ''' convert a list of list- or array-type objects to internal
        Point class'''
        return [Point(point[0], point[1]) for point in points]
    
    def as_lists(self, clusters):
        ''' 
        converts the Points in each cluster back into regular feature
        vectors (lists) and ids. It returns a list of tuples containing
        the id of that point and its feature vector. 
        '''
        clusters_as_points = {}
        for cluster, members in clusters.iteritems():
            clusters_as_points[cluster] = [ (member.id, member.feature_vector)  for member in members]
        return clusters_as_points
    
    def print_points(self, points):
        ''' a weird klugey function for printing lists of points. ''' 
        s = ''
        for p in points:
            s += str(p) + '\n'
        return s[:-2]
    
    
    def immediate_neighbours(self, point, all_points):
        ''' find the immediate neighbours of point.'''
        # XXX TODO: this is probably a stupid way to do it; if we could
        # use a grid approach it should make this much faster.
        neighbours = []
        for p in all_points:
            if p == point:
                # you cant be your own neighbour...!
                continue
            d = self.distance(point.feature_vector,p.feature_vector)
            if d < self.epsilon:
                neighbours.append(p)
        return neighbours
    
    def add_connected(self, points, all_points, current_cluster):
        ''' find every point in the set of all_points which are
        density-connected, starting with the initial points list. '''
        cluster_points = []
        for point in points:
            if not point.visited:
                point.visited = True
                new_points = self.immediate_neighbours(point, all_points)
                if len(new_points) >= self.min_pts:                                
                    # append any new points on the end of the list we're
                    # already iterating over.
                    for p in new_points:
                        if p not in points:
                            points.append(p)
    
            # here, we separate 'visited' from cluster membership, since
            # 'visited' only helps keep track of if we've checked this
            # point for neighbours. it may or may not have been assessed
            # for cluster membership at that point.
            if not point.cluster:
                cluster_points.append(point)
                point.cluster = current_cluster
        if self.debug: 
            print 'Added points %s' % self.print_points(cluster_points)
        return cluster_points
    
    def dbscan(self):
        ''' Main dbscan algorithm function. pass in a list of feature
        vectors (most likely a list of lists or a list of arrays), a
        radius epsilon within which to search for neighbouring points, and
        a min_pts, the minimum number of neighbours a point must have
        within the radius epsilon to be considered connected. the default
        distance metric is euclidean''' 
    
        assert isinstance(self.points, list)
        epsilon = float(self.epsilon)
        if not isinstance(self.points[0], Point):
            # only check the first list instance. imperfect, but the lists
            # could be arbitrarily long.
            points = self._as_points(self.points)

        if self.debug:
            print '\nEpsilon: %.2f' % epsilon
            print 'Min_Pts: %d' % self.min_pts
        
        clusters = {}     # each cluster is a list of points
        clusters[-1] = [] # store all the points deemed noise here. 
        current_cluster = -1
        for point in points:
            if not point.visited:
                point.visited = True
                neighbours = self.immediate_neighbours(point, points)
                if len(neighbours) >= self.min_pts:
                    current_cluster += 1
                    if self.debug: 
                        print '\nCreating new cluster %d' % (current_cluster)
                        print '%s' % str(point)
                    point.cluster = current_cluster                
                    cluster = [point,]
                    cluster.extend(self.add_connected(neighbours, points, current_cluster))
                    clusters[current_cluster] = cluster
                else:
                    clusters[-1].append(point)
                    if self.debug: 
                        print '\nPoint %s has no density-connected neighbours.' % str(point.feature_vector)
    
        # return the dictionary of clusters, converting the Point objects
        # in the clusters back to regular lists
        return self.as_lists(clusters)
    
    def run(self, epsilon, min_pts, distance=euclidean, debug=False, pca=False):
        '''
        Runs the DBSCAN algorithm.
        '''
        #Re-initialise clusters
        if self.clusters != []:
            self.clusters = []
            
        if self.td_matrix == None:
            self.construct_term_doc_matrix(pca=pca)
        #Ugly code to transform a numpy array to a list
        matrix = []
        for row_index, doc_id in enumerate(self.document_dict.keys()):
            #Along with the feature vector we append the document id as well
            matrix.append( (list(self.td_matrix[row_index]), doc_id) )
                
        self.points = matrix
        self.epsilon = epsilon
        self.min_pts = min_pts
        self.distance = distance
        self.debug = debug
        clusters = self.dbscan()
        self.split_documents(clusters)
            
        return clusters
    
    def split_documents(self, clusters):
        '''
        This method splits the whole collection of documents 
        of this data set into the different clusters. Of course
        the algorithm should have been run first and then invoke this method.
        It takes as input the clusters of document ids.
        '''
        for cluster, members in clusters.iteritems():
            documents = OrderedDict()
            for member in members:
                doc_id = member[0]
                document = self.document_dict[doc_id]            
                documents[doc_id] = document
            self.clusters.append(Cluster(cluster, documents))
            
#######################################################################
# HELPER CLASSES
#######################################################################
class Point(object):
    ''' internal helper class to support algorithm implementation'''
    def __init__(self,feature_vector, id):
        # feature vector should be something like a list or a numpy
        # array
        self.feature_vector = feature_vector
        self.cluster = None
        self.visited = False
        self.id = id

    def __str__(self):
        return str(self.feature_vector)