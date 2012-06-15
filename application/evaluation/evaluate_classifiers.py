'''
Created on 21 Mar 2012

@author: george
'''
import pylab, time, numpy#!@UnresolvedImport 
from matplotlib.font_manager import FontProperties#!@UnresolvedImport 
fontP = FontProperties()
fontP.set_size(45)
from database.warehouse import WarehouseServer
from analysis.classification.tree import TreeClassifier
from analysis.classification.knn import kNNClassifier
from evaluation.evaluators import ClassificationEvaluator
from database.model.agents import *

def run_evaluation():
    
    iterations = 20 #how many times will we run the classification ti get the average results
    
    average = []
    for i in range(iterations):
        classifiers = [TreeClassifier(), kNNClassifier()] 
        results = []
        for classifier in classifiers:
            train_set = numpy.array([author for author in TrainingAuthor.objects])
            ce = ClassificationEvaluator(train_set, ['celebrity', 'media', 'journalist', 'activist', 'commoner'])  
            res =  ce.evaluate(classifier, K=10)
            fs = []
            for r in res:
                fs.append(r[2])
            results.append(fs)
        average.append(results)
    
    
    c1 = []
    c2 = []
    for a in average:
        c1.append(a[0])
        c2.append(a[1])
        
    av1 = [sum(a)/iterations for a in zip(*c1)]
    av2 = [sum(a)/iterations for a in zip(*c2)]
    results = [av1, av2]
    
    N = 5
    ind = numpy.arange(N)  # the x locations for the groups
    width = 0.15       # the width of the bars
    
    pylab.subplot(111)
    rects1 = pylab.bar(ind, results[0], width,
                        color='r')
    
    rects2 = pylab.bar(ind+width, results[1], width,
                        color='y')
    
    # add some
    pylab.ylabel('F metric')
    pylab.title('Classification accuracy per user type ')
    pylab.xticks(ind+width, ('Celebrity', 'Media organisation', 'Journalist', 'Activist', 'Common people') )
    
    pylab.legend( (rects1[0], rects2[0]), ('Decision Trees', 'k-Nearest') )
    
    pylab.show()
    
import cProfile    
cProfile.run('run_evaluation()', 'different_classifiers')
