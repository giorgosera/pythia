# -*- coding: utf-8 -*-
'''
Created on 14 Nov 2011

@author: george

This file contains useful functions used throughout the application.
'''
import re, math, chardet, bingtrans, enchant, itertools#!@UnresolvedImport
import twitter_text#!@UnresolvedImport
import AlchemyAPI#!@UnresolvedImport
import numpy
from matplotlib.dates import date2num#!@UnresolvedImport
from lxml import etree#!@UnresolvedImport
from StringIO import StringIO
from nltk.stem.porter import PorterStemmer #!@UnresolvedImport

###########################################
# GLOBALS                                #
###########################################
d = enchant.Dict("en_US")
bingtrans.set_app_id('5521E4A630094D968D49B39B6511A0A76CB025E1')
alchemyObj = AlchemyAPI.AlchemyAPI()
alchemyObj.setAPIKey("d7605e69dd3d2d7a032f11272d9b000e77d43545");
ignorewords = set(['rt', 'via', 'jan25', 'egypt', 'cairo', '25jan', "s", ":)", ":(", ":p", "25"\
                '(' , ')', '<', '>', '#', '@', '?', '!', '.', ',', '=', '|', \
                '&', ':', '+', '\'', '\'ve',"m", 're', '-', '"', '."', '...', '..', '--', '[', ']' ])


def strip_url(text):
    #return re.compile(r'(\w+:\/\/\S+)').sub('', text)
    #return re.compile(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(([‌​^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""", re.DOTALL).sub('',text)
    urls = extract_urls(text)
    for url in urls:
        text=' '.join(re.sub(url['url']," ",text).split())
    return text

def extract_urls(text):
    extractor = twitter_text.Extractor(text)
    urls = []
    for um in extractor.extract_urls_with_indices():
        urls.append(um)
    return urls

def strip_mentions(text):
    return re.compile(r'@[\s,_,A-Z,a-z]+').sub('',text)


def strip_hashtags(text):
    return re.compile(r'#[\s]?[,A-Z,a-z,0-9]+[\s]?').sub('',text)
    
def strip_html(html):
    return re.compile(r'<[^>]+>').sub('',html)
    
def split_alpha(text):    
    return re.compile(r'[^A-Z^a-z]+').split(text)

def turn_lowercase(text):
    return [word.lower() for word in text if word!=''] 

def detect_encoding(text):
    try:
        text = unicode(text).encode('utf-8')
        encoding = chardet.detect(text)
    except Exception, e:
        print e
    else:    
        if encoding['encoding'] == 'ascii':
            return 'ascii'
        else:
            return 'unicode'
        
def translate_text(text, src='ar', tgt='en'):
    translation = text
    #===========================================================================
    # try:
    #    detected = parse_result(alchemyObj.TextGetLanguage(text), "iso-639-1")
    #    src = detected[0]['iso-639-1']
    # except Exception, e:
    #    print e
    #    src = 'en'    
    #===========================================================================
    
    if src != 'en': 
        try:
            translation =  bingtrans.translate(text, src, tgt)            
        except ValueError:
            pass
    return translation       

def text_stemming(text):
    return PorterStemmer().stem_word(text)

def detect_english(text):
    return d.check(text)

def tfidf(token_occurences, no_of_tokens, no_of_docs, token_appears_in):
    '''
    Claculates the tf-idf score for a token.
    '''
    tf = float(token_occurences) / float(no_of_tokens)
    idf = math.log(float(no_of_docs) / float(token_appears_in))
    return tf*idf

def is_a_retweet(tweet):
    '''
    A regular expression is used to identify retweets. Note that 
    Twitter identifies retweets either with "RT" followed by username
    or "via" followed by username. 
    '''
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    match = rt_patterns.search(tweet)
    if match != None:
        return True
    else:
        return False

def get_mentions(tweet):
    '''
    A regular expression is used to identify mentions.
    '''
    extractor = twitter_text.Extractor(tweet)
    entities = []
    for um in extractor.extract_mentioned_screen_names_with_indices():
        entities.append(um)
    return entities

def parse_result(result, type):
    '''
    Parses the result returned from Alchemy and constructs
    and dict.
    '''
    context = etree.iterparse(StringIO(result))
    object_dict = {}
    objects = []
    for action, elem in context:
        if not elem.text:
            text = "None"
        else:
            text = elem.text
        object_dict[elem.tag] = text
        if elem.tag in type:
            objects.append(object_dict)
            object_dict = {}
    return objects

def aggregate_data(dates, cumulative):
    '''
    This method aggregates the dates into buckets and the buckets'
    size depends on the desired resolution. i.e. if resolution is 
    an hour then the dates belonging to the same day will fall in the 
    same bucket. 
    '''        
    x = sorted([date2num(item) for item in dates]) 
    grouped_dates = numpy.array([[d, len(list(g))] for d, g in itertools.groupby(x)])
    dates, counts = grouped_dates.transpose()
    if cumulative:
        counts = counts.cumsum()
    return dates, counts