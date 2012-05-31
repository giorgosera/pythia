'''
Created on 22 Jan 2012

@author: george
'''
import numpy, nltk
import orange, Orange #!@UnresolvedImport
from math import sqrt
from c_extensions import euclidean as cython_euclidean#!@UnresolvedImport
from c_extensions import cosine as cython_cosine#!@UnresolvedImport
###########################################
## Similarity and distance measures      ##
###########################################

def jaccard(v1, v2):
    '''
    Due to the idiosyncracies of my code the jaccard index is a bit 
    altered. The theory is the same but the implementation might be a bit 
    weird. I do not have two vectors containing the words of both documents
    but instead I have two equally sized vectors. The columns of the vectors 
    are the same and represent the words in the whole corpus. If an entry
    is 1 then the word is present in the document. If it is 0 then it is not present.
    SO first we find the indices of the words in each documents and then jaccard is 
    calculated based on the indices.
    '''
    indices1 = numpy.nonzero(v1>0.0)[0]
    indices2 = numpy.nonzero(v2==1.0)[0]

    dist = nltk.metrics.distance.jaccard_distance(set(indices1), set(indices2))
    return dist
    
def pearson(v1,v2):
    # Simple sums
    sum1=sum(v1)
    sum2=sum(v2)
    
    # Sums of the squares
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])    
    
    # Sum of the products
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
    
    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
    if den==0: 
        return 0
    
    return 1.0-num/den

def cosine(v1,v2, distance=True):
    '''
    Calculates the cosine similarity between two vectors. If distance == True we
    return the similarity multiplied by -1 in order to indicate that lower
    distances are closer similarities. The cosine sim of two close vectors
    should be almost 1 but in our clustering algorithm we take distances so
    1 must become -1 to indicate a closer distance. 
    '''
    #===========================================================================
    # sim = numpy.dot(v1, v2)  / (sqrt(numpy.dot(v1, v1) * numpy.dot(v2, v2))) 
    # if distance:
    #    dist = 1-sim
    # else:
    #    dist = sim
    #===========================================================================
    dist = cython_cosine.distance(v1, v2)
    return dist 
     
     
def tanimoto(v1,v2):
    '''
    Calculates the tanimoto coeeficient between two vectors. 
    '''
    count_v1,count_v2,common=0,0,0
    
    for i in range(len(v1)):
        if v1[i]!=0: count_v1+=1 # in v1
        if v2[i]!=0: count_v2+=1 # in v2
        if v1[i]!=0 and v2[i]!=0: common+=1 # in both
    return 1.0-(float(common)/(count_v1+count_v2-common))

def euclidean(x,y):
    ''' 
    Calculate the euclidean distance between x and y.
    '''
    # sqrt((x0-y0)^2 + ... (xN-yN)^2)
    assert len(x) == len(y)
    return cython_euclidean.distance(x, y)

def slow_euclidean(x,y):
    ''' 
    Calculate the euclidean distance between x and y. This is the slow
    version. I just included it for future reference
    '''
    # sqrt((x0-y0)^2 + ... (xN-yN)^2)
    assert len(x) == len(y)
    sum = 0.0
    length_x = len(x)
    for i in xrange(length_x):
        sum += (x[i] - y[i])**2
    return sqrt(sum)

#################ORANGE OVERRIDEN DISTANCE METHODS #########################

class ExamplesDistance_Cosine(orange.ExamplesDistance):
    def __init__(self, *args):
        orange.ExamplesDistance.__init__(self, *args)
    def __call__(self, ex1, ex2):
        ex1 = numpy.fromiter(list(ex1), dtype=numpy.float)
        ex2 = numpy.fromiter(list(ex2), dtype=numpy.float)
        return cosine(ex1,ex2, distance=True)

class ExamplesDistanceConstructor_Cosine(orange.ExamplesDistanceConstructor):
    def __init__(self, *args):
        orange.ExamplesDistanceConstructor.__init__(self, *args)
    def __call__(self, *args):
        return ExamplesDistance_Cosine()
    
class ExamplesDistance_Jaccard(orange.ExamplesDistance):
    def __call__(self, ex1, ex2):
        '''
        Note that ex1 is the centroid feature vector and ex2 is the actual example. 
        So the best we can do is assume that if an entry in ex1 is not zero then that word appears
        in the cluster. So we search for non-zero elements in ex1 and elements == 1 in ex2.
        '''
        ex1 = numpy.fromiter(list(ex1), dtype=numpy.float)
        ex2 = numpy.fromiter(list(ex2), dtype=numpy.float)
        
        return jaccard(ex1,ex2)

class ExamplesDistanceConstructor_Jaccard(orange.ExamplesDistanceConstructor):
    def __init__(self, *args):
        orange.ExamplesDistanceConstructor.__init__(self, *args)
    def __call__(self, data):
        indxs = [i for i, a in enumerate(data.domain.attributes) \
                 if a.varType==Orange.data.Type.Continuous]
        return ExamplesDistance_Jaccard(domain=data.domain, indxs=indxs)
