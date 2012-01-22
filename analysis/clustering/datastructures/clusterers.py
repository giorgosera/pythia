'''
Created on 21 Jan 2012

@author: george
'''

class AbstractClusterer(object):
    '''
    This is the abstract clusterer and specialized clusterers
    must be derived from it. 
    '''

    def __init__(self):
        '''
        Constructs a new clusterer object
        '''
        pass
    
    def print_it(self):
        raise NotImplementedError('algo is not implemented.')
 
class Biclusterer(AbstractClusterer):
    '''
    A biclusterer class. 
    '''

    def __init__(self, vector, left=None, right=None, similarity=0.0, id=None):
        '''
        Constructs a biclusterer
        '''
        AbstractClusterer.__init__(self)
        self.left = left
        self.right = right
        self.vector = vector
        self.similarity = similarity
        self.id = id 

    def print_it(self, labels=None, n=0):
        '''
        This method outputs the clusters in a human readable form.
        '''
        # For each new cluster have a small indentation to make it look hierarchical  
        for i in range(n): 
            print ' ',
        if self.id<0:
            # This is a branch
            print '-'
        else:
            # This is an root node
            if labels==None: print self.id
            else: print labels[self.id]
            
        # Recursively traverse the left and right branches
        if self.left!=None: 
            self.left.print_it(labels=labels,n=n+1)
        if self.right!=None: 
            self.right.print_it(labels=labels,n=n+1)