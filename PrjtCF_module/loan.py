import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from pandas.tseries.offsets import Day, MonthEnd
import datetime as dt
from datetime import datetime
from datetime import timedelta
from datetime import date
from functools import wraps

import genfunc
from index import Index
from account import Account, Merge


class Loan(object):
    def __init__(self,
                 index = None, # Index class
                 amt_ntnl = None, # float
                 rate_fee = None, # float
                 rate_IR = None, # float
                 title = None, # string : "LoanA"
                 tag = None, # string tuple : ("tagA", "tagB")
                 note = "" # string
                 ):
        # index 입력
        if isinstance(index, Index):
            self.cindex = index
            self.index = index.index
            
        # 주요 변수 입력
        self.amt_ntnl = amt_ntnl
        self.rate_fee = rate_fee
        self.rate_IR = rate_IR
            
        # title 입력
        self.title = title
        
        # tag 입력 : tag는 튜플로 받음. string으로 입력된 경우 튜플로 변환 필요
        if isinstance(tag, tuple):
            self.tag = tag
        elif isinstance(tag, str):
            self.tag = tuple(tag)
        elif tag is None:
            self.tag = None
        else:
            raise ValueError("tag is not a tuple")
            
        # note 입력
        self.note = note
        
        # Account Setting
        self.ntnl = Account(self.cindex, self.title, self.tag)
        self.fee = Account(self.cindex, self.title, self.tag)
        self.IR = Account(self.cindex, self.title, self.tag)
        
        # Initialize
        self._intlz()
        
    def _intlz(self):
        # 초기화 함수 실행
        dct = {}
        
        self.ntnl.amt = self.amt_ntnl
        self.ntnl.subscdd(self.cindex.index[0], self.ntnl.amt)
        self.ntnl.addscdd(self.cindex.index[-1], self.ntnl.amt)
        dct['ntnl'] = self.ntnl
        
        self.fee.rate = self.rate_fee
        self.fee.amt = self.ntnl.amt * self.fee.rate
        self.fee.addscdd(self.cindex.index[0], self.fee.amt)
        dct['fee'] = self.fee
        
        self.IR.rate = self.rate_IR
        self.IR.amt = self.ntnl.amt * self.IR.rate
        self.IR.addscdd(self.cindex.index, np.ones(len(self.cindex)) * self.IR.amt)
        dct['IR'] = self.IR
        
        self.loan = Merge(dct)
        
    #####################################################
    # fee 입금 함수, IR 입금 함수, ntnl 출금, 입금 함수 추가 필요 #
        