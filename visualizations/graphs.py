'''
Created on 5 Feb 2012

@author: george
'''
import itertools, numpy
import matplotlib.pyplot as plt#!@UnresolvedImport
#matplotlib.use('GTKAgg')
from matplotlib.dates import date2num, num2date#!@UnresolvedImport
from matplotlib import ticker#!@UnresolvedImport

class Timeline(object):
    '''
    A simple 2D graph depicting the growth of a variable 
    as a function of time. 
    '''

    def __init__(self, data, cumulative=False):
        '''
        Constructor method. The data should provide 
        a datetime field.
        '''
        self.data = data
        self.cumulative = cumulative
        
    def _format_date(self, x, pos):
        return num2date(x).strftime('%Y-%m-%d %H:%M:%S')
        #lambda numdate, _: num2date(numdate).strftime('%Y-%m-%d %H:%M:%S')
        
    def plot(self):
        '''
        First calls a function to aggregate data into time buckets and then
        holds the figure in case we want to plot multiple lines.
        '''
        dates, counts = self._aggregate_data()
        plt.plot(dates, counts, 'o-')             
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(self._format_date))
        plt.gcf().autofmt_xdate()        
        plt.hold(True)
    
    def show(self):
        plt.show()
        plt.hold(False)
    
    def _aggregate_data(self):
        '''
        This method aggregates the data into buckets and the buckets'
        size depends on the desired resolution. i.e. if resolution is 
        an hour then the data belonging to the same day will fall in the 
        same bucket. 
        '''        
        x = sorted([date2num(item) for item in self.data]) 
        grouped_dates = numpy.array([[d, len(list(g))] for d, g in itertools.groupby(x)])
        dates, counts = grouped_dates.transpose()
        if self.cumulative:
            counts = counts.cumsum()
        return dates, counts
        