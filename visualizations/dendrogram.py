'''
Created on 22 Jan 2012

@author: george
'''
from PIL import Image, ImageDraw #!@UnresolvedImport 

class Dendrogram(object):
    '''
    This is the data structure for a dendrogram. Hierarchical clustering can be easily 
    visualized using a dendrogram.
    '''

    def __init__(self, cluster, labels, filename, height, depth):
        '''
        Constructs a dendrogram.
        '''
        self.cluster = cluster
        self.labels = labels
        self.filename = filename
        self.height = height*20
        self.width = 1200
        #width is fixed at 1200
        self.scaling = float(self.width-150)/depth
        
        self.img = Image.new('RGB',(self.width,self.height), (255, 255, 255))
        self.drawobj = ImageDraw.Draw(self.img)
        
        self.drawobj.line((0, self.height/2, 10, self.height/2), fill=(255, 0, 0))
        
        self.draw_node(10, self.height/2)
        
        self.img.save(filename, 'JPEG')
        
    def draw_node(self, x, y):
        '''
        Draws a node of the dendrogram. The code is adopted from Programming Collective 
        Intelligence by Toby Segaran.
        '''
        if self.cluster.id<0:
            h1=self.cluster.left.get_height()*20
            h2=self.cluster.right.get_height()*20
            top = y - (h1+h2)/2
            bottom = y + (h1+h2)/2
            # Line length
            ll=self.cluster.similarity*self.scaling
            # Vertical line from this cluster to children    
            self.drawobj.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))    
            
            # Horizontal line to left item
            self.drawobj.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))    
        
            # Horizontal line to right item
            self.drawobj.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))        
        
            # Call the function to draw the left and right nodes
            temp = self.cluster
            self.cluster = self.cluster.left
            self.draw_node(x+ll,top+h1/2)
            self.cluster = temp.right
            self.draw_node(x+ll,bottom-h2/2)
            self.cluster = temp
        else:   
            # If this is an endpoint, draws the appropriate label
            self.drawobj.text((x+5,y-7),self.labels[self.cluster.id],(0,0,0))
        