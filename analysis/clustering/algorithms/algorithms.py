'''
Created on 22 Jan 2012

@author: george
'''

from analysis.clustering.structures import Bicluster
from math import sqrt
import numpy, random, math

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
    cluster = [Bicluster(data[i], id=i) for i in range(len(data))]
            
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
        newcluster= Bicluster(mergevec,left=cluster[lowestpair[0]],
                             right=cluster[lowestpair[1]],
                             similarity=closest,id=curr_clust_id)
    
        # cluster ids that weren't in the original set are negative
        curr_clust_id-=1
        del cluster[lowestpair[1]]
        del cluster[lowestpair[0]]
        cluster.append(newcluster)
        
    return cluster[0]


def kmeans(data, similarity=pearson, k = 10):
    '''
    This method performs k-means clustering. The user selects the similarity 
    measure and the number of clusters k to be used. 
    '''
    # Determine the minimum and maximum values for each point
    ranges=[(min([d[i] for d in data]),max([d[i] for d in data])) 
            for i in range(len(data[0]))]

    #We assign k randomly placed centroids
    clusters = [[ random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0]
                 for i in range(len(data[0]))] for j in range(k)]

    lastmatches = None 
    #The algorithm will run for maximum 100 iterations
    for t in range(100):
        print "Iteration %d" %t
        bestmatches = [[] for i in range(k)]
        
        #Find the closest centroid for each row in data
        for j in range(len(data)):
            d = data[j]
            bestmatch = 0
            for i in range(k):
                distance = similarity(clusters[i], d)
                if distance < similarity(clusters[bestmatch], d):
                    bestmatch = i
            bestmatches[bestmatch].append(j)
        
        #This is a termination condition. If the last matches are the same as 
        #this iteration's ones then we must have reached the equilibrium.
        if bestmatches==lastmatches:
            break
        lastmatches = bestmatches    
        
        #The last step of the iteration is to move the centroids to their new positions
        for i in range(k):
            average = [0.0]*len(data[0])
            if len(bestmatches[i])>0:
                for d in bestmatches[i]:
                    for m in range(len(data[d])):
                        average[m] += data[d][m]
                for j in range(len(average)):
                    average[j] /= len(bestmatches[i])
                clusters[i]=average
     
    return bestmatches