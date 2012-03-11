# -*- coding: utf-8 -*-
'''
Created on 5 Feb 2012

@author: george
'''
import datetime
from mongoengine import *
from database.model.tweets import *
connect("pythia_db")
    
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

###############################################################################################
#AUTHOR INITIALIZATION TEST DOCUMENTS
############################################################################################### 
def get_author_initialisation_data():
    documents = [["Police are making a move to contain. Minor clashes breaking out. #egypt #jan", "ianinegypt", "http://twitter.com/ianinegypt/status/29882051620503552", 14],
                 ["Protesters calm down for call to prayer. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/29888160099999744", 16],
                 ["Police using water canons on demonstrators in tahrir. #egypt #jan25 protesters throwing rocks", "ianinegypt", "http://twitter.com/ianinegypt/status/29897528803594240", 15],
                 ["Police beating protesters, protesters respond with rocks. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/29897831477157888", 13],
                 ["Protesters keep out flanking police. Police now surrounded. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/29898774176333824", 15],
                 ["To shouts of allah akbar, police are retreating and regrouping. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/29899637716426752", 10] ,
                 ["Police use tear gas on demonstrators. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/29901410996850690", 11],
                 ["Police flat outnumbered and out flanked PERIOD #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/29900862507720704", 11],
                 ["protesters calling for same revolution as in #tunisia Police have yet to challenge them. #jan25 #egypt", "ianinegypt", "http://twitter.com/ianinegypt/status/29877711912566784", 2],
                 ["Twitter problems in #Egypt. I am using a proxy. Expect a video from @dailynewsegypt on today's demonstration. #Jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/29963090992828416", 8],
                 ["RT @Sarahcarr: RT @mand0z: The son of @ayman_nour  Noor Ayman Noor @Noor1Noor2 has been arrested and sent to unknown location", "ianinegypt", "http://twitter.com/ianinegypt/status/30051842821984257", 6],
                 ["This morning's police presence downtown isn't as tight... We'll see what today brings. #jan25 #Egypt", "ianinegypt", "http://twitter.com/ianinegypt/status/30156031812182016", 22],
                 ["Protest scheduled for 9 AM in Tahrir square.  On my way to cover it. #Egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30156558721622016", 32],
                 ["VIDEO: Check out yesterday's and last night's action in Cairo  http://bit.ly/hvIgd0 and http://bit.ly/gO4Zer #Egypt #Jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30201952587489280", 6],
                 ["Very heavy security in Tahrir, no protests. Aside from security, #Egypt looks like business as usual. #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30218377481949184", 19],
                 ["RT @AymanM: death toll in #egypt clashes #jan25 has risen to 4 people, 150 civilians injured according to interior min", "ianinegypt", "http://twitter.com/aymanm/status/30223227179507712", 33] ,
                 ["RT @3arabawy: New post: #Jan25 Marching on State Security Police HQ in Mansoura http://bit.ly/dUy94O", "ianinegypt", "http://twitter.com/3arabawy/status/30240899690668033", 9],
                 ["Protesters stop chanting for call to prayer. Less than 100 at press syndicate. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30250741482397696", 1] ,
                 ["Protesters clashing with  police at press syndicate. Still small numbers. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30254614779531264", 12],
                 ["Protest growing angrily and with numbers at press syndicate.#jan25 #egypt", "ianinegypt", "http://twitter.com/ianinegypt/status/30257044036517888", 12] ,
                 ["Protests at both lawyers and press syndicates heating up #jan25 #egypt", "ianinegypt", "http://twitter.com/ianinegypt/status/30260918378045440", 13],
                 ["Situation deteriorating downtown. Calm with sporadic violence but tense. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30264871656366080", 14],
                 ["Police fortifying lawyers syndicate. #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30272375824056321", 4],
                 ["Fires burning on Galaa street. Tear gas being used on protesters. #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30281144561831936", 18] ,
                 ["Tear gas not stopping protesters, police in full retreat #jan25 #egypt", "ianinegypt", "http://twitter.com/ianinegypt/status/30284522440368128", 41],
                 ["Hundreds fill street looks like marching to Tahrir. #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30290985036546050", 23],
                 ["Protesters change direction. Going towards corniche. they are pushing a smoldering dumpster #jan25.", "ianinegypt", "http://twitter.com/ianinegypt/status/30293413572116481", 9],
                 ["Things are quieter after police made mass arrest. Rumors of demonstration in Tahrir at 7. #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30303678099361794", 24],
                 ["Reports coming from Suez, live bullets, molotov cocktails. Things seem to be deteriorating very quickly there. #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30328671235477506", 34],
                 ["Police arresting people standing around in Tahrir, Sadat metro below Tahrir is closed. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30332820400377856", 24],
                 ["Protests still taking place downtown.  Tomorrow I will be traveling to Suez to cover events there. #jan25 #Egypt", "ianinegypt", "http://twitter.com/ianinegypt/status/30363574580805632", 18],
                 ["RT @Amiralx: RT @RamyRaoof: hotline numbers 4 legal aid & requesting lawyers 0193150442 - 0163447782 - 0107030030 - 0120624003 #Egypt #Jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30363796186861568", 11], 
                 ["Protesters moving along corniche towards ministry of foreign affairs. #jan25 #egypt", "ianinegypt", "http://twitter.com/ianinegypt/status/29872689501970432", 4],
                 ["I am doing the same RT @3arabawy: Twitter and facebook are not stable at all. I can't access them at the moment. I'm back to proxy.. #Egypt", "ianinegypt", "http://twitter.com/ianinegypt/status/30382880421060608", 12] ,
                 ["RT @arabist: TBC RT @moselim: Unconfirmed reports that the Egyptian Army has descended on #Suez streets. #Egypt #Mubarak", "ianinegypt", "http://twitter.com/arabist/status/30384822903906305", 24],
                 ["On my way to report on the events in Suez. Hopefully I won't be turned around at a police checkpoint. #jan25 #Egypt", "ianinegypt", "http://twitter.com/ianinegypt/status/30523945115455489", 16],
                 ["My cab driver says he isn't protesting because he needs to make money for food. But Friday he plans to hit the street. #egypt #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30529087093084161", 44],
                 ["U.S. Embassy spokesperson says, they are pressuring the Egyptian government to release all journalists. Helped free 8 yesterday. #jan25", "ianinegypt", "http://twitter.com/ianinegypt/status/30542937997705216", 35],
                 ["RT @bencnn: To watch: increasingly lukewarm western, espec. US, expressions of support for Pres Mubarak--whom they backed for decades. #Jan25 #Egypt", "ianinegypt", "http://twitter.com/bencnn/status/30541850263687168", 36],
                 ]
    
    docs = []

    for document in documents:
        content = Content()
        content.raw = document[0]
        doc = TestTweet()
        doc.author_screen_name = document[1]
        doc.content = content
        doc.url = document[2]
        doc.retweet_count = document[3]
        doc.save()
        docs.append(doc)
    return docs