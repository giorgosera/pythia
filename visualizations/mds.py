'''
Created on 22 Jan 2012

@author: george
'''
import pylab#!@UnresolvedImport 
from tools.orange_utils import construct_distance_matrix, orange_mds
import matplotlib.cm as cm#!@UnresolvedImport 

class MDS(object):
    '''
    Uses multidimensional scaling (MDS) to visualize clusters. 
    For more info see: http://orange.biolab.si/doc/modules/orngMDS.htm
    or http://orange.biolab.si/doc/reference/Orange.projection.mds/#Orange.projection.mds.MDS
    '''
    def __init__(self, data):
        '''
        Constructor
        '''
        self.data = data
    
    def plot(self, classes_list=None, class_col_name=None, color=None):
        '''
        Projects the data points using MDS.
        Optionally we can input with the classes names in order to 
        plot the points painted according to their class.
        '''
        distance = construct_distance_matrix(self.data)
        mds = orange_mds(distance)
        
        labelled = classes_list != None and class_col_name != None
        colors = ["red", "yellow", "blue"]
        # Construct points (x, y, instanceClass)
        points = []
        for (i, d) in enumerate(self.data):
            if labelled:
                points.append((mds.points[i][0], mds.points[i][1], d.get_metas(str)[class_col_name].value))
            else:
                points.append((mds.points[i][0], mds.points[i][1], 0))

        # Paint each class separately
        if labelled:
            for c in classes_list:
                sel = filter(lambda x: x[-1] == str(c), points)
                x = [s[0] for s in sel]
                y = [s[1] for s in sel]
                if len(classes_list) > 1:
                    pylab.scatter(x, y, c=cm.jet(float(c)/(len(classes_list)-1)))
                else:
                    pylab.scatter(x, y, c=cm.jet(1))
        else:
            sel = filter(lambda x: x[-1] == 0, points)
            x = [s[0] for s in sel]
            y = [s[1] for s in sel]
            pylab.scatter(x, y, c=colors[0])

        pylab.show()