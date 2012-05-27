'''
Created on 22 Mar 2012

@author: george

This script allow us to annotate known events with their labels
'''
import datetime
from database.warehouse import WarehouseServer
from mongoengine import connect
connect("pythia_db")
from evaluation.evaluators import ExtrinsicClusteringEvaluator
ws = WarehouseServer()

from_date=datetime.datetime(2011, 01, 25, 12, 20, 0)
to_date=datetime.datetime(2011, 01, 25, 12, 25, 0)
tweet_list = ws.get_documents_by_date(from_date, to_date)
ce = ExtrinsicClusteringEvaluator(tweet_list)
ce.annotate_dataset()