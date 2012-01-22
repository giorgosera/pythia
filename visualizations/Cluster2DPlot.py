'''
Created on 22 Jan 2012

@author: george
'''
from analysis.clustering.algorithms.algorithms import pearson
from PIL import Image, ImageDraw #!@UnresolvedImport 
import random, math

class Cluster2DPlot(object):
    '''
    Uses multidimensional scaling to visualize clusters in 2D. Code adopted from
    Programming Collective Intelligence.
    '''

    def __init__(self, data, labels, filename, similarity=pearson, rate=0.01):
        '''
        Constructor
        '''
        self.data = data
        self.similarity=similarity
        self.rate = rate
        self.labels = labels
        self.filename = filename
    
    def draw(self):
        '''
        Draws a 2D plot of the clusters.
        '''
        self._scale_down()
        img=Image.new('RGB',(2000,2000),(255,255,255))
        draw=ImageDraw.Draw(img)
        for i in range(len(self.data)):
            x=(self.data[i][0]+0.5)*1000
            y=(self.data[i][1]+0.5)*1000
            draw.text((x,y),self.labels[i],(0,0,0))
        img.save(self.filename,'JPEG')
    
    def _scale_down(self):
        '''
        Performs multidimensional scaling.
        '''
        n=len(self.data)

        # The real distances between every pair of items
        realdist=[[self.similarity(self.data[i],self.data[j]) for j in range(n)] 
             for i in range(0,n)]
        
        # Randomly initialize the starting points of the locations in 2D
        loc=[[random.random(),random.random()] for i in range(n)]
        fakedist=[[0.0 for j in range(n)] for i in range(n)]
        
        lasterror=None
        for m in range(0,1000):
            # Find projected distances
            for i in range(n):
                for j in range(n):
                    fakedist[i][j]=math.sqrt(sum([pow(loc[i][x]-loc[j][x],2) 
                                       for x in range(len(loc[i]))]))
        
            # Move points
            grad=[[0.0,0.0] for i in range(n)]
          
            totalerror=0
            for k in range(n):
                for j in range(n):
                    if j==k: continue
                    # The error is percent difference between the distances
                    errorterm=(fakedist[j][k]-realdist[j][k])/realdist[j][k]
              
                    # Each point needs to be moved away from or towards the other
                    # point in proportion to how much error it has
                    grad[k][0]+=((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
                    grad[k][1]+=((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm
        
                    # Keep track of the total error
                    totalerror+=abs(errorterm)
        
            # If the answer got worse by moving the points, we are done
            if lasterror and lasterror<totalerror: break
            lasterror=totalerror
          
            # Move each of the points by the learning rate times the gradient
            for k in range(n):
                loc[k][0] -= self.rate*grad[k][0]
                loc[k][1] -= self.rate*grad[k][1]
        
        return loc