'''
Created on 19 Mar 2012

@author: george
'''
import datetime
from database.model.tweets import EvaluationTweet
from database.warehouse import WarehouseServer
from mongoengine import connect
connect("pythia_db")

ws = WarehouseServer()

class EventDetectionEvaluator(object):
    '''
    This class is responsible for performing event detection
    evaluation.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.tweets = None
        
    def annotate_dataset(self):
        '''
        If the test dataset has not been annotated yet, then by calling this 
        function one can start annotating events manually.
        '''
        from_date=datetime.datetime(2011, 01, 25, 12, 0, 0)
        to_date=datetime.datetime(2011, 01, 25, 12, 10, 0)
        tweet_list = ws.get_documents_by_date(from_date, to_date)
        print 'Hey lucky guy...you have to annotate',len(tweet_list),"tweets!"
        for tweet in tweet_list:
            print tweet.content.raw
            accept = raw_input("Accept? (Y or N)")
            if accept == "N": 
                continue
            elif accept == "Y":
                et = EvaluationTweet()
                et = tweet
                avail_events = et.get_available_events()
                for event in avail_events:
                    print event.event_class, event.event_desc
                event_class = raw_input("What is the class of this event?")
                et.event_class = event_class
                
if __name__ == "__main__":
    ede = EventDetectionEvaluator()
    ede.annotate_dataset()