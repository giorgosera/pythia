'''
Created on 5 Feb 2012

@author: george
'''
import datetime, json, os, numpy
import matplotlib.pyplot as plt#!@UnresolvedImport
#matplotlib.use('GTKAgg')
from matplotlib.dates import num2date#!@UnresolvedImport
from matplotlib import ticker#!@UnresolvedImport
from string import Template
from tools.utils import aggregate_data

class Timeline(object):
    '''
    A simple 2D graph depicting the growth of a variable 
    as a function of time. 
    '''

    def __init__(self, dates, counts, meta=None, cumulative=False):
        '''
        Constructs a timeline object. It takes as input the 
        dates (x-axis), the counts (y-axis) and optionally 
        a meta dictionary which contains meta information for the plot.
        '''
        self.dates = dates
        self.counts = counts
        self.meta = meta

    def plot(self):
        raise NotImplementedError('plot is not implemented.')
    
class D3Timeline(Timeline):
    '''
    A timeline based on d3.js
    '''
    def plot(self, url='timeline_growth.html'):
        '''
        Parses the data and aggregate them in case they are not. Aggregation 
        basically groups dates (x-axis) with counts (y-axis). The data is 
        passed to a javascript file which then renders the timeline. In order
        to see the result navigate to your browser to the url specified as input.  
        '''
        json_data = {'dates': self.dates, "counts": self.counts, 'meta': self.meta}
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        template = os.path.join(os.getcwd(), '../visualizations/templates/timeline_main_hackathon.html')
        #template = os.path.join(os.getcwd(), '../visualizations/templates/timeline.html')

        html = Template(open(template).read())
        html = html.substitute(items=json.dumps(json_data, default=dthandler))
        f = open(os.path.join(os.getcwd(), '../visualizations/templates', os.path.basename('../visualizations/templates/'+url)), 'w')
        f.write(html)
        f.close()

class MatplotlibTimeline(Timeline):
    '''
    Produces a timeline with matplotlib.
    '''
    def _format_date(self, x, pos):
        return num2date(x).strftime('%Y-%m-%d %H:%M:%S')
        
    def plot(self):
        '''
        First calls a function to aggregate data into time buckets and then
        holds the figure in case we want to plot multiple lines.
        '''
        plt.plot(self.dates, self.counts, 'o-')             
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(self._format_date))
        plt.gcf().autofmt_xdate()        
        plt.hold(True)
    
    def show(self):
        plt.show()
        plt.hold(False)    
        