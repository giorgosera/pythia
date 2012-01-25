# -*- coding: utf-8 -*-
'''
Created on 14 Nov 2011

@author: george

This file contains useful functions used throughout the application.
'''
import re
import chardet, bingtrans #!@UnresolvedImport

def strip_url(text):
    return re.compile(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(([‌​^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""", re.DOTALL).sub('',text)
    
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
    bingtrans.set_app_id('5521E4A630094D968D49B39B6511A0A76CB025E1')
    translation =  bingtrans.translate(text, src, tgt)            
    return translation         
