'''
Created on 5 Feb 2012

@author: george
'''
import itertools, numpy, datetime, json, os
import matplotlib.pyplot as plt#!@UnresolvedImport
#matplotlib.use('GTKAgg')
from matplotlib.dates import date2num, num2date#!@UnresolvedImport
from matplotlib import ticker#!@UnresolvedImport
from string import Template

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

    def plot(self):
        raise NotImplementedError('plot is not implemented.')
    
class D3Timeline(Timeline):
    '''
    A timeline based on d3.js
    '''
    def plot(self):
        dates = []
        counts = []
        for d in self.data:
            t_dates, t_counts = aggregate_data(d, self.cumulative)
            dates.append([num2date(date).strftime('%Y-%m-%d %H:%M:%S') for date in t_dates])
            counts.append(t_counts)
        dates = dates
        counts = [count.tolist() for count in counts]
                      
        json_data = {'dates': dates, "counts": counts}
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        template = os.path.join(os.getcwd(), '../visualizations/templates/timeline.html')
        
        html = Template(open(template).read())
        html = html.substitute(items=json.dumps(json_data, default=dthandler))
        f = open(os.path.join(os.getcwd(), '../visualizations/templates', os.path.basename('../visualizations/templates/timeline_appended.html')), 'w')
        f.write(html)
        f.close()

class MatplotlibTimeline(Timeline):
    '''
    Produces a timeline with matplotlib.
    '''
    def _format_date(self, x, pos):
        return num2date(x).strftime('%Y-%m-%d %H:%M:%S')
        #lambda numdate, _: num2date(numdate).strftime('%Y-%m-%d %H:%M:%S')
        
    def plot(self):
        '''
        First calls a function to aggregate data into time buckets and then
        holds the figure in case we want to plot multiple lines.
        '''
        dates, counts = aggregate_data(self.data, self.cumulative)
        plt.plot(dates, counts, 'o-')             
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(self._format_date))
        plt.gcf().autofmt_xdate()        
        plt.hold(True)
    
    def show(self):
        plt.show()
        plt.hold(False)      
        
          
####################################################
# HELPER METHODS
####################################################          
def aggregate_data(data, cumulative):
    '''
    This method aggregates the data into buckets and the buckets'
    size depends on the desired resolution. i.e. if resolution is 
    an hour then the data belonging to the same day will fall in the 
    same bucket. 
    '''        
    x = sorted([date2num(item) for item in data]) 
    grouped_dates = numpy.array([[d, len(list(g))] for d, g in itertools.groupby(x)])
    dates, counts = grouped_dates.transpose()
    if cumulative:
        counts = counts.cumsum()
    return dates, counts