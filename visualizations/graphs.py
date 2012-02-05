'''
Created on 5 Feb 2012

@author: george
'''
import matplotlib.pyplot as plt#!@UnresolvedImport
import matplotlib#!@UnresolvedImport
matplotlib.use('GTKAgg')
from matplotlib.dates import date2num, num2date#!@UnresolvedImport
from matplotlib import ticker#!@UnresolvedImport
import itertools

class Timeline(object):
    '''
    A simple 2D graph depicting the growth of a variable 
    as a function of time. 
    '''

    def __init__(self, data):
        '''
        Constructor method. The data should provide 
        a datetime field.
        '''
        self.data = data
        
    def plot(self):
        grouped_data = self._aggregate_data()
        plt.plot([h[0] for h in grouped_data], [h[1] for h in grouped_data], 'o-')
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda numdate, _: num2date(numdate).strftime('%Y-%d-%m %H:%M:%S')))
        plt.gcf().autofmt_xdate()        
        plt.show()
    
    def _aggregate_data(self):
        '''
        This method aggregates the data into buckets and the buckets'
        size depends on the desired resolution. i.e. if resolution is 
        an hour then the data belonging to the same day will fall in the 
        same bucket. 
        '''        
        x = sorted([date2num(item) for item in self.data]) 
        return [[d, len(list(g))] for d, g in itertools.groupby(x)]
        