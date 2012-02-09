# -*- coding: utf-8 -*-
'''
Created on 5 Feb 2012

@author: george
'''
import datetime

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
    
    
    entry1 = {"tokens":doc1_tokens, "raw": doc1_raw, "word_frequencies":freq1}
    entry2 = {"tokens":doc2_tokens, "raw": doc2_raw, "word_frequencies":freq2}
    entry3 = {"tokens":doc3_tokens, "raw": doc3_raw, "word_frequencies":freq3}
    
    doc1 = TestDocument(0, "test_name", "test_name", datetime.datetime.utcnow, entry1, "no_url", 0)
    doc2 = TestDocument(1, "test_name", "test_name", datetime.datetime.utcnow, entry2, "no_url", 0)
    doc3 = TestDocument(2, "test_name", "test_name", datetime.datetime.utcnow, entry3, "no_url", 0)    
    expected = {'0': entry1, '1': entry2, '2': entry3}  
    
    return expected, [doc1_raw, doc2_raw, doc3_raw], [doc1, doc2, doc3]

def get_unicode_document():
    content = {'tokens': [u'test'], 'raw': u'This is a test', 'word_frequencies': [(u'test', 1)]}
    doc = TestDocument(0, "test_name", "test_name", datetime.datetime.utcnow, content, "no_url", 0)
    return "This is a test", 'هذا هو اختبار'

###############################################################################################
#CLUSTERING TESTS DATA
###############################################################################################    
def get_orange_clustering_test_data():
    content0 = {'tokens': ['document', 'relat', 'sport', 'footbal', 'basketbal', 'tenni', 'golf', 'etc'], 'raw': 'This is a document related to sports : Football, basketball, tennis, golf etc.', 'word_frequencies': [('basketbal', 1), ('document', 1), ('etc', 1), ('footbal', 1), ('golf', 1), ('relat', 1), ('sport', 1), ('tenni', 1)]}
    content1 = {'tokens': ['document', 'talk', 'basketbal', 'footbal', 'tenni', 'golf', 'sport', 'gener'], 'raw': 'In this document we will be talking about basketball, football, tennis, golf and sports in general.', 'word_frequencies': [('basketbal', 1), ('document', 1), ('footbal', 1), ('gener', 1), ('golf', 1), ('sport', 1), ('talk', 1), ('tenni', 1)]}
    content2 = {'tokens': ['like', 'golf', 'footbal', 'realli', 'amaz', 'sport', 'love', 'love', 'basketbal', 'tenni'], 'raw': 'I like golf but football is really an amazing sport. I love it. But I love basketball too and tennis', 'word_frequencies': [('love', 2), ('amaz', 1), ('basketbal', 1), ('footbal', 1), ('golf', 1), ('like', 1), ('realli', 1), ('sport', 1), ('tenni', 1)]}
    content3 = {'tokens': ['document', 'relat', 'program', 'specif', 'python', 'cpp', 'info', 'check', 'blog'], 'raw': 'This document is related to programming. More specifically Python and CPP. For more info check my blog.', 'word_frequencies': [('blog', 1), ('check', 1), ('cpp', 1), ('document', 1), ('info', 1), ('program', 1), ('python', 1), ('relat', 1), ('specif', 1)]}
    content4 = {'tokens': ['wrote', 'small', 'python', 'script', 'run', 'cluster', 'algorithm', 'hope', 'work', 'well', 'ill', 'tri', 'cpp'], 'raw': 'I wrote a small Python script to run a clustering algorithm. I hope it works well . If not Ill try CPP', 'word_frequencies': [('algorithm', 1), ('cluster', 1), ('cpp', 1), ('hope', 1), ('ill', 1), ('python', 1), ('run', 1), ('script', 1), ('small', 1), ('tri', 1), ('well', 1), ('work', 1), ('wrote', 1)]}
    content5 = {'tokens': ['blog', 'write', 'python', 'program', 'gener'], 'raw': 'This blog writes about Python and programming in general.', 'word_frequencies': [('blog', 1), ('gener', 1), ('program', 1), ('python', 1), ('write', 1)]}
    doc0 = TestDocument(0, "test_name", "test_name", datetime.datetime.utcnow, content0, "no_url", 0)
    doc1 = TestDocument(1, "test_name", "test_name", datetime.datetime.utcnow, content1, "no_url", 0)
    doc2 = TestDocument(2, "test_name", "test_name", datetime.datetime.utcnow, content2, "no_url", 0)   
    doc3 = TestDocument(3, "test_name", "test_name", datetime.datetime.utcnow, content3, "no_url", 0)
    doc4 = TestDocument(4, "test_name", "test_name", datetime.datetime.utcnow, content4, "no_url", 0) 
    doc5 = TestDocument(5, "test_name", "test_name", datetime.datetime.utcnow, content5, "no_url", 0)     
    return [doc0, doc1, doc2, doc3, doc4, doc5]