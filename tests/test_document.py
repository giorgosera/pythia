# -*- coding: utf-8 -*-
'''
Created on 5 Feb 2012

@author: george
'''
import datetime
from database.model.tweets import Content

class TestDocument(object):
    
    def __init__(self, id, author_screen_name, author_name, date, content, url, retweet_count ):
        self.id = id
        self.author_screen_name = author_screen_name
        self.author_name = author_name
        self.date = date
        self.content = content
        self.url = url
        self.retweet_count = retweet_count 


###############################################################################################
#TEXT ANALYSIS TESTS DATA
###############################################################################################    
def get_test_documents():
    doc1_raw = 'frequent FrEquEnt frequent <li>word</li> word sentence sentence' 
    doc2_raw = 'sentence <a href="www.google.com">arab</a> spring'
    doc3_raw = 'a is not a toKENIzed document'               
    
    doc1_tokens = ['frequent', 'frequent', 'frequent', 'word', 'word', 'sentenc', 'sentenc']
    doc2_tokens = ['sentenc', 'arab', 'spring']
    doc3_tokens = ['token', 'document']
    
    freq1 = [('frequent', 3), ('sentenc', 2), ('word', 2)]
    freq2 = [('arab', 1), ('sentenc', 1), ('spring', 1)]
    freq3 = [('document', 1), ('token', 1)]
    
    content1 = Content()
    content1.raw = doc1_raw
    content1.tokens = doc1_tokens
    content1.construct_word_freq_list(freq1)
    content1.date = datetime.datetime.utcnow
    
    content2 = Content()
    content2.raw = doc2_raw
    content2.tokens = doc2_tokens
    content2.construct_word_freq_list(freq2)
    content2.date = datetime.datetime.utcnow
    
    content3 = Content()
    content3.raw = doc3_raw
    content3.tokens = doc3_tokens
    content3.construct_word_freq_list(freq3)
    content3.date = datetime.datetime.utcnow
    
    doc1 = TestDocument(0, "test_name", "test_name", datetime.datetime.utcnow, content1, "no_url", 0)
    doc2 = TestDocument(1, "test_name", "test_name", datetime.datetime.utcnow, content2, "no_url", 0)
    doc3 = TestDocument(2, "test_name", "test_name", datetime.datetime.utcnow, content3, "no_url", 0)    
    expected = {'0': content1, '1': content2, '2': content3}  
    
    return expected, [doc1_raw, doc2_raw, doc3_raw], [doc1, doc2, doc3]

def get_unicode_document():
    content = {'tokens': [u'test'], 'raw': u'This is a test', 'word_frequencies': [(u'test', 1)]}
    doc = TestDocument(0, "test_name", "test_name", datetime.datetime.utcnow, content, "no_url", 0)
    return "This is a test", 'هذا هو اختبار'

###############################################################################################
#CLUSTERING TESTS DATA
###############################################################################################    
def get_orange_clustering_test_data():
    content0 = Content()
    content0.raw = 'This is a document related to sports : Football, basketball, tennis, golf etc.'
    content0.tokens = ['document', 'relat', 'sport', 'footbal', 'basketbal', 'tenni', 'golf', 'etc']
    content0.construct_word_freq_list([('basketbal', 1), ('document', 1), ('etc', 1), ('footbal', 1), ('golf', 1), ('relat', 1), ('sport', 1), ('tenni', 1)])
    content0.date = datetime.datetime.utcnow
    
    content1 = Content()
    content1.raw = 'In this document we will be talking about basketball, football, tennis, golf and sports in general.'
    content1.tokens = ['document', 'talk', 'basketbal', 'footbal', 'tenni', 'golf', 'sport', 'gener']
    content1.construct_word_freq_list([('basketbal', 1), ('document', 1), ('footbal', 1), ('gener', 1), ('golf', 1), ('sport', 1), ('talk', 1), ('tenni', 1)])
    content1.date = datetime.datetime.utcnow
    
    content2 = Content()
    content2.raw = 'I like golf but football is really an amazing sport. I love it. But I love basketball too and tennis'
    content2.tokens = ['like', 'golf', 'footbal', 'realli', 'amaz', 'sport', 'love', 'love', 'basketbal', 'tenni']
    content2.construct_word_freq_list([('love', 2), ('amaz', 1), ('basketbal', 1), ('footbal', 1), ('golf', 1), ('like', 1), ('realli', 1), ('sport', 1), ('tenni', 1)])
    content2.date = datetime.datetime.utcnow
    
    content3 = Content()
    content3.raw = 'This document is related to programming. More specifically Python and CPP. For more info check my blog.'
    content3.tokens = ['document', 'relat', 'program', 'specif', 'python', 'cpp', 'info', 'check', 'blog']
    content3.construct_word_freq_list([('blog', 1), ('check', 1), ('cpp', 1), ('document', 1), ('info', 1), ('program', 1), ('python', 1), ('relat', 1), ('specif', 1)])
    content3.date = datetime.datetime.utcnow
    
    content4 = Content()
    content4.raw = 'I wrote a small Python script to run a clustering algorithm. I hope it works well . If not Ill try CPP'
    content4.tokens = ['wrote', 'small', 'python', 'script', 'run', 'cluster', 'algorithm', 'hope', 'work', 'well', 'ill', 'tri', 'cpp']
    content4.construct_word_freq_list([('algorithm', 1), ('cluster', 1), ('cpp', 1), ('hope', 1), ('ill', 1), ('python', 1), ('run', 1), ('script', 1), ('small', 1), ('tri', 1), ('well', 1), ('work', 1), ('wrote', 1)])
    content4.date = datetime.datetime.utcnow
    
    content5 = Content()
    content5.raw = 'This blog writes about Python and programming in general.'
    content5.tokens = ['blog', 'write', 'python', 'program', 'gener']
    content5.construct_word_freq_list([('blog', 1), ('gener', 1), ('program', 1), ('python', 1), ('write', 1)])
    content5.date = datetime.datetime.utcnow
    
    doc0 = TestDocument(0, "test_name", "test_name", datetime.datetime.utcnow, content0, "no_url", 0)
    doc1 = TestDocument(1, "test_name", "test_name", datetime.datetime.utcnow, content1, "no_url", 0)
    doc2 = TestDocument(2, "test_name", "test_name", datetime.datetime.utcnow, content2, "no_url", 0)   
    doc3 = TestDocument(3, "test_name", "test_name", datetime.datetime.utcnow, content3, "no_url", 0)
    doc4 = TestDocument(4, "test_name", "test_name", datetime.datetime.utcnow, content4, "no_url", 0) 
    doc5 = TestDocument(5, "test_name", "test_name", datetime.datetime.utcnow, content5, "no_url", 0)     
    return [doc0, doc1, doc2, doc3, doc4, doc5]