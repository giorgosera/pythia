'''
Created on 21 Mar 2012

@author: george
'''
import numpy
from database.warehouse import WarehouseServer
from analysis.classification.tree import TreeClassifier
from database.model.agents import TrainingAuthor
from evaluation.evaluators import ClassificationEvaluator

ws = WarehouseServer()
authors = ws.get_all_documents(type=TrainingAuthor)
ce = ClassificationEvaluator(authors, ["Celebrity", "Media", "Journalists", "Activists", "Commoner"])
metrics = ce.evaluate(classifier_type=TreeClassifier, K=10)
print metrics