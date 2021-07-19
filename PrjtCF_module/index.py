import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from pandas.tseries.offsets import Day, MonthEnd
from datetime import datetime
from datetime import timedelta
from datetime import date
from functools import wraps

import genfunc


class Index(object):
    def __init__(self,
                start: Day = None,
                end: Day = None,
                periods: int = None,
                freq: str = None
                ) -> None:
        self.start = start
        self.end = end
        self.periods = periods
        self.freq = freq
        self._range = pd.date_range(self.start, self.end, self.periods, self.freq)
        self._idxno = np.arange(len(self._range))
        
    def __getitem__(self, no):
        return self.index[no]
        
    def __len__(self):
        return len(self.index)
        
    @property
    def index(self):
        return self._range.date
        
    @property
    def year(self):
        return self._range.year
        
    @property
    def month(self):
        return self._range.month
        
    @property
    def day(self):
        return self._range.day
        
    @property
    def idxno(self):
        return self._idxno
        
    def idxloc(self, year=None, month=None, day=None):
        """
        Return boolean array of data(year, month, day) is in array
        """
        isyear = _getblnloc(self.year, year)
        ismonth = _getblnloc(self.month, month)
        isday = _getblnloc(self.day, day)
        
        return isyear & ismonth & isday
        

def _getblnloc(array, val):
    if val == None:
        return [True]
    else:
        return booleanloc(array)[val]


class booleanloc():
    """
    Return boolean array of data is in array
    
    Parameters
    ----------
    array : data array
    
    Returns
    -------
    array : boolean array
    
    Examples
    --------
    tmp = booleanloc(np.array([10, 20, 30]))
    tmp[10]
    >>> array([True, False, False])
    tmp[[20, 30]]
    >>> array([False, True, True])
    """
    def __init__(self, array):
        self.array = array
        
    def __getitem__(self, data):
        if genfunc.is_iterable(data):
            return self.loopiniter(self.array, data)
        else:
            return self.array == data
    
    @staticmethod
    def loopiniter(array, data):
        tmp = [False]
        for val in data:
            blnarray = array == val
            tmp = tmp | blnarray
        return tmp
        
        
        