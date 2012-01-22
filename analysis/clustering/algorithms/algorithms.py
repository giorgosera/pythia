'''
Created on 22 Jan 2012

@author: george
'''

from analysis.clustering.datastructures.clusterers import Biclusterer
from math import sqrt
import numpy

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

def cosine(v1,v2):
    '''
    Calculates the cosine similarity between two vectors. In the end we
    return the similarity multiplied by -1 in order to indicate that lower
    distances are closer similarities. The cosine sim of two close vectors
    should be almost 1 but in our clustering algorithm we take distances so
    1 must become -1 to indicate a closer distance. 
    '''
    sim = numpy.dot(v1, v2) / (sqrt(numpy.dot(v1, v1)) * sqrt(numpy.dot(v2, v2))) 
    return (-1*sim + 1) / 2.0
###########################################
## Clustering algorithms                 ##
###########################################

def hierarchical(data, similarity=pearson):
    '''
    This method performs hierarchical clustering. It is given a set of data 
    points to be clustered and the similarity metric to be used. It returns 
    the top cluster since it references the two other clusters which have been 
    merged to create it and then each one of them references other two etc. So we
    can just traverse it recursively to get all the clusters. By default Pearson similarity
    is used to measure distances but others can be used too by giving other measures as 
    input.
    '''
    distances = {}
    curr_clust_id = -1
    
    #Initially all the data points are considered as clusters. 
    cluster = [Biclusterer(data[i], id=i) for i in range(len(data))]
            
    while len(cluster) > 1:
        lowestpair = (0, 1)
        closest = similarity(cluster[0].vector, cluster[1].vector)
  
        #Calculates distances for all clusters
        for i in range(len(cluster)):
            for j in range(i+1, len(cluster)):
                if (cluster[i].id, cluster[j].id) not in distances:
                    distances[(cluster[i].id, cluster[j].id)] = similarity(cluster[i].vector, cluster[j].vector)
                d = distances[cluster[i].id, cluster[j].id]
                if d < closest:
                    closest = d 
                    lowestpair = (i, j)
                    
        #After a cluster is merge we compute its new centroid as the avergae of the merged clusters.
        mergevec=[(cluster[lowestpair[0]].vector[i]+cluster[lowestpair[1]].vector[i])/2.0 
                  for i in range(len(cluster[0].vector))]
    
        # create the new cluster
        newcluster= Biclusterer(mergevec,left=cluster[lowestpair[0]],
                             right=cluster[lowestpair[1]],
                             similarity=closest,id=curr_clust_id)
    
        # cluster ids that weren't in the original set are negative
        curr_clust_id-=1
        del cluster[lowestpair[1]]
        del cluster[lowestpair[0]]
        cluster.append(newcluster)
        
    return cluster[0]
