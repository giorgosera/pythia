'''
Created on 22 Jan 2012

@author: george
'''
import numpy, random, math, scipy
from math import sqrt

###########################################
## Similarity measures                   ##
###########################################

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
    sim = numpy.dot(v1, v2) / (sqrt(numpy.dot(v1, v1)) * sqrt(numpy.dot(v2, v2))) 
    if distance:
        return (-1*sim + 1) / 2.0
    else:
        return sim
     
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
    ''' calculate the euclidean distance between x and y.'''
    # sqrt((x0-y0)^2 + ... (xN-yN)^2)
    assert len(x) == len(y)
    sum = 0.0
    for i in xrange(len(x)):
        sum += pow(x[i] - y[i],2)
    return sqrt(sum)