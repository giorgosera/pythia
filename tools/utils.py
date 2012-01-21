'''
Created on 14 Nov 2011

@author: george

This file contains useful functions used throughout the application.
'''
import re

def strip_html(html):
    return re.compile(r'<[^>]+>').sub('',html)
    
def split_alpha(text):    
    return re.compile(r'[^A-Z^a-z]+').split(text)

def turn_lowercase(text):
    return [word.lower() for word in text if word!=''] 

def create_word_count_file(filename, word_list):
    '''
    Creates a file containing a matrix of word counts and documents
    i.e
    
    ########################################################################
    #            "hello" | "this" | "is" | "a" | "word" | "count" | "matrix"
    # George        1    |  0     |   5  |  6  |    1   |   6     |   6
    # Chuck         3    |  1     |   3  |  3  |    0   |   0     |   4
    # .....................................................................
    #########################################################################  
    '''
    pass
#    out=file(filename,'w')
#    out.write('Blog')
#    for word in word_list: 
#        out.write('\t%s' % word)
#    
#    out.write('\n')
#    for blog,wc in wordcounts.items():
#        print blog
#        out.write(blog)
#        for word in wordlist:
#            if word in wc: out.write('\t%d' % wc[word])
#            else: out.write('\t0')
#        out.write('\n') 