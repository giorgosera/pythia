'''
Created on 14 Nov 2011

@author: george

This module is responsible to deal with graph operations
'''
import networkx as nx  #!@UnresolvedImport
import re

class GraphBuilder(object):
    '''
    This is an abstract class for graph structures. All other
    graphs should be derived from this.
    '''
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def get_graph(self):
        '''
        Must be implemented by the concrete classes
        '''
        raise NotImplementedError("get_graph() is not implemented.") 
    

class RetweetGraphBuilder(GraphBuilder):    
    '''
    This class implements a graph depicting retweet relationships.
    '''
    def __init__(self, tweet_list):
        GraphBuilder.__init__(self)
        self.tweets = tweet_list    
    
    def get_graph(self):
        return self.graph
        
    def _get_rt_sources(self, tweet):
        '''
        Identifies the sources of retweets. It is supposed to be a private
        method. Should not be called from outside.
        '''
        rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
        return [ source.strip()
                    for tuple in rt_patterns.findall(tweet)
                        for source in tuple
                            if source not in ("RT", "via") ]    
        
    def construct_graph_from_retweets(self):
        '''
        The function receives a list of retweet tuples of the form 
        and constructs the digraph between retweet origins.
        '''
        for tweet in self.tweets:
            rt_sources = self._get_rt_sources(tweet["text"])
            if not rt_sources: continue
            for rt_source in rt_sources:
                self.graph.add_edge(rt_source, tweet["from_user"], {"tweet_id" : tweet["id"]})
            