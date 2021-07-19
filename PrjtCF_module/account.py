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


class Account(object):
    def __init__(self,
                 index = None, # Index class
                 title = None, # string : "ProductA"
                 tag = None, # string tuple : ("tagA", "tagB")
                 bal_strt = 0, # int
                 note = "" # string
                 ):
        # index 입력
        if isinstance(index, Index):
            self.cindex = index
            self.index = index.index
            
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
            
        # bal_strt 입력
        self.bal_strt = bal_strt
        
        # note 입력
        self.note = note
        
        # Initialize
        self._intlz()

    def _intlz(self):
        # 초기화 함수 실행
        self.setdf()
        self.setjnl()
    
    #### INITIAL SETTING FUNCTION #### 초기화 함수
    DFCOL = ['add_scdd', 'add_scdd_cum', 'sub_scdd', 'sub_scdd_cum',
             'bal_strt', 'amt_add', 'amt_add_cum', 
             'amt_sub', 'amt_sub_cum', 'bal_end',
             'add_rsdl_cum', 'sub_rsdl_cum']
    JNLCOL = ['amt_add', 'amt_sub', 'note']
    def setdf(self):
        # DataFrame 초기화
        self.df = pd.DataFrame(np.zeros([len(self.index), len(self.DFCOL)]),
                               columns = self.DFCOL, 
                               index = self.index)
        self.df.loc[self.index[0], 'bal_strt'] = self.bal_strt
        
        # balance 계산 실행
        self._cal_bal()
        
    def setjnl(self):
        # Journal(분개장) 초기화
        self.jnl = pd.DataFrame(columns = self.JNLCOL)
    #### INITIAL SETTING FUNCTION ####
    
    #### DECORATOR ####
    def listwrapper(func):
        @wraps(func)
        def wrapped(self, *args):
            is_iter = True
            for arg in args:
                if genfunc.is_iterable(arg) is False:
                    is_iter = False
            if is_iter is True:
                ilen = len(args[0])
                for i in range(ilen):
                    new_args = []
                    for val in args:
                        new_args = new_args + [val[i]]
                    new_args = tuple(new_args)
                    func(self, *new_args)
            else:
                new_args = args
                func(self, *new_args)
        return wrapped
    #### DECORATOR ####
     
    #### CALCULATE DATA BALANCE ####
    def _cal_bal(self):
        # 누적합 계산
        self.df.loc[:, 'add_scdd_cum'] = self.df.loc[:, 'add_scdd'].cumsum()
        self.df.loc[:, 'sub_scdd_cum'] = self.df.loc[:, 'sub_scdd'].cumsum()
        self.df.loc[:, 'amt_add_cum'] = self.df.loc[:, 'amt_add'].cumsum()
        self.df.loc[:, 'amt_sub_cum'] = self.df.loc[:, 'amt_sub'].cumsum()
        
        # 계좌 잔액 계산
        for i, idx in enumerate(self.index):
            if i > 0:
                self.df.loc[idx, 'bal_strt'] = self.df.loc[self.index[i-1], 'bal_end']
            self.df.loc[idx, 'bal_end'] = self.df.loc[idx, 'bal_strt'] \
                                          + self.df.loc[idx, 'amt_add'] \
                                          - self.df.loc[idx, 'amt_sub']
        
        # 누적 합 차액 계산
        self.df.loc[:, 'add_rsdl_cum'] = self.df.loc[:, 'add_scdd_cum'] \
                                         - self.df.loc[:, 'amt_add_cum']
        self.df.loc[:, 'sub_rsdl_cum'] = self.df.loc[:, 'sub_scdd_cum'] \
                                         - self.df.loc[:, 'amt_sub_cum']
    #### CALCULATE DATA BALANCE ####
        
    
    #### INPUT DATA ####
    @listwrapper
    def addscdd(self, index, amt):
        self.df.loc[index, 'add_scdd'] += amt
        self._cal_bal()

    @listwrapper
    def subscdd(self, index, amt):
        self.df.loc[index, 'sub_scdd'] += amt
        self._cal_bal()
        
    @listwrapper
    def addamt(self, index, amt):
        # 분개장(journal)에 데이터 입력
        tmpjnl = pd.DataFrame([[amt, 0, "add_amt"]], \
                              columns=self.JNLCOL, index=[index])
        self.jnl = pd.concat([self.jnl, tmpjnl])
        
        # DataFrame에 데이터 입력
        self.df.loc[index, 'amt_add'] += amt
        
        # Balance 계산 실행
        self._cal_bal()
        
    @listwrapper
    def subamt(self, index, amt):
        # 분개장(journal)에 데이터 입력
        tmpjnl = pd.DataFrame([[0, amt, "sub_amt"]], \
                              columns=self.JNLCOL, index=[index])
        self.jnl = pd.concat([self.jnl, tmpjnl])
        
        # DataFrame에 데이터 입력
        self.df.loc[index, "amt_sub"] += amt
        
        # Balance 계산 실행
        self._cal_bal()
        
    @listwrapper
    def iptamt(self, index, amt):
        # amt가 양수인 경우 addamt 실행, 음수인 경우 subamt 실행
        if amt >= 0:
            self.addamt(index, amt)
        else:
            self.subamt(index, -amt)
    #### INPUT DATA ####


class Merge(object):
    def __init__(self, dct:dict):
        # dictionary : {"nameA":A, "nameB":B, ...}
        self.dct = dct
    
    @property
    def df(self):
        # merge 완료된 dataframe 출력
        tmp_dct = sum([self.dct[x].df for x in self.dct])
        return tmp_dct
    
    def df_col(self, col):
        # column명 구분에 따라 dictionary 데이터를 취합
        tmp_dct = pd.DataFrame({x: self.dct[x].df.loc[:, col] for x in self.dct})
    
    def title(self):
        # dictionary 데이터 상 title 값 취합
        tmp_dct = pd.Series({x: self.dct[x].title for x in self.dct})
        return tmp_dct
    
    def tag(self):
        # dictionary 데이터 상 tag 값 취합
        tmp_dct = pd.Series({x: self.dct[x].tag for x in self.dct})
        return tmp_dct
    
    def note(self):
        # dictionary 데이터 상 note 값 취합
        tmp_dct = pd.Series({x: self.dct[x].note for x in self.dct})
        return tmp_dct


class _idxsrch:
    def __init__(self) -> None:
        self._name = None
    
    def __set_name__(self, owner, name):
        self._name = name
        
    def __set__(self, instance, value):
        instance.__dict__[self._name] = value
        
        

    