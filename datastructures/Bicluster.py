'''
Created on 20 Dec 2011

@author: george
'''

class Bicluster(object):
    '''
    This data structure represents a dendrogram node
    '''
    def __init__(self, vector, left=None, right=None, distance=0.0, id=None):
        self.left=left
        self.right=right
        self.vec=vector
        self.id=id
        self.distance=distance
        