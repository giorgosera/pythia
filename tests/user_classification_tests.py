'''
Created on 26 Jan 2012

@author: george
'''
import unittest, numpy
from database.warehouse import WarehouseServer
from database.model.agents import *
from analysis.classification.tree import TreeClassifier

from mongoengine import connect
connect("pythia_db")

class Test(unittest.TestCase):

    def test_author_classification_dummy_dataset(self):
       
        train_set = numpy.array([[0.2, 0.5, 0.2,  0.2, 0.1,  10.,  0],
                                [0.2, 0.3, 0.12, 0.1, 0.1,  10.,  0],
                                [0.2, 0.2, 0.08, 0.2, 0.01, 20.,  0],
                                [0.2, 0.5, 0.1,  0.1, 0.2,  5.,   0],
                                [0.2, 0.1, 0.2,  0.2, 0.3,  20.,  0],
                                [0.7, 0.5, 0.2,  0.8, 0.3,  0.1, 1],
                                [0.6, 0.8, 5.2,  0.2, 0.6,  0.3, 1],
                                [0.2, 0.6, 8.2,  0.9, 0.9,  0.1, 1],
                                [0.5, 0.9, 1.2,  0.1, 0.1,  0.2, 1],
                                [0.9, 0.1, 0.9,  0.6, 0.3,  0.6, 1]])
        
        attributes = ["retweets", "links", "retweeted", "replies", "mentions", "ff-ratio", "class"]
        
        classifier = TreeClassifier()
        classifier.train(train_set, attributes)
        example = [0.2, 0.5, 0.2,  0.2, 0.1,  100,  0]
        prediction = classifier.classify(example)    
        self.assertEquals(0, prediction.value)
        
    def test_author_classification_real_dataset(self):
        # 0 --> Celebrirty
        # 1 --> Media
        # 2 --> Journalists
        # 3 --> Common people
        classifier = TreeClassifier()
        train_set = numpy.array([[0.18, 0.57, 0.01,  0.053, 0.0,  52872.,  0], #Bill Gates
                                [0.5, 0.1, 0.0, 0.09, 0.0,  151.,  0], #Justin Bieber
                                [0.096, 0.4, 0.06, 0.2, 0.0, 14052.,  0], #Ashton Kutcher
                                [0.06, 0.051, 0.04,  0.62, 0.0,  216342.,   0], #Oprah
                                [0.026, 0.72, 0.03,  0.07, 0.0,  79183.,  0], #Amy Winehouse
                                [0.006, 0.85, 0.52,  0.0, 0.0,  55025., 1], #BBC
                                [0.17, 0.77, 0.86,  0.03, 0.0,  5540., 1], #CNN
                                [0.25, 0.73, 2.,  0.0, 0.0,  264., 1], #HuffPost
                                [0.02, 0.99, 0.79,  0.03, 0.0,  5034., 1], #AlJazeera
                                [0.13, 0.31, 2.2,  0.33, 0.0,  14., 2], #Ali Velshi
                                [0.19, 0.19, 2.8,  0.17, 0.0,  4., 2], #MujMash 
                                [0.053, 0.23, 2.5,  0.3, 0.0,  12., 2], #StevePoliti
                                [0.09, 0.16, 11.3,  0.36, 0.0,  8., 2], #Rachel King
                                [0.4, 0.36, 8.6,  0.16, 0.0,  0.32, 3], #George Eracleous
                                [0.2, 0.12, 7.1,  0.35, 0.0,  0.38, 3], #Nik Adhia
                                [0.26, 0.15, 2.4,  0.31, 0.0,  0.9, 3], #A person
                                [0.55, 0.13, 13.2,  0.25, 0.0,  0.7, 3]]) #Yet another person
        
        attributes = ["retweets", "links", "retweeted", "replies", "mentions", "ff-ratio", "class"]
        classifier.train(train_set, attributes)
        celebrity_example = [0.096, 0.3, 0.03,  0.08, 0.0,  94258,  0]
        media_example = [0.0, 0.8, 0.89,  0.031, 0.0,  184.,  0]
        common_example = [0.55, 0.13, 13.2,  0.25, 0.0,  0.7,  0]   
        journalist_example = [0.24, 0.48, 14.7,  0.11, 0.0,  11.9,  0]    
        prediction_celebrity = classifier.classify(celebrity_example)
        prediction_media = classifier.classify(media_example)
        prediction_journalist = classifier.classify(journalist_example)
        prediction_common = classifier.classify(common_example)
        calculated = [prediction_celebrity, prediction_media, prediction_journalist, prediction_common]
        expected = [0, 1, 2, 3]
        self.assertEqual(expected, calculated)
        #orngTree.printTree(treeClassifier)
        
    def test_author_classification_egypt_dataset(self):
        TestAuthor.drop_collection()    
        ws = WarehouseServer()      
        for author in [author for author in ws.get_authors(type=Author)]:
            if len(author.tweets) > 200:
                t = TestAuthor()
                t.screen_name = author.screen_name
                t.tweets = author.tweets
                t.save()
            
        
        authors = ws.get_authors(type=TestAuthor)
        for author in authors:
            print '-----------------------'
            print author.screen_name
            vector = author.update_feature_vector()
            print vector
        
        classifier = TreeClassifier()
        attributes = ["retweets", "links", "retweeted", "replies", "mentions", "ff-ratio", "class"]
        train_set = numpy.array([author.get_feature_vector_with_type() for author in TrainingAuthor.objects])

        classifier.train(train_set, attributes)
        
        for author in authors:
            prediction = "No prediction"
            if len(author.feature_vector) > 0:
                prediction = classifier.classify(author.get_feature_vector_with_type())
            print author.screen_name
            print prediction
            print '----------------------'
            
        TestAuthor.drop_collection()   
        
                 
if __name__ == "__main__":
    unittest.main()