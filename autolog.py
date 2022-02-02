import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
from tqdm import tqdm
import pickle
import yfinance as yf

def autolog():
    vix = yf.Ticker("^VIX")
    previous_close = vix.info['previousClose']
    fifty_day_avg = vix.info['fiftyDayAverage']
    twohundred_day_avg = vix.info['twoHundredDayAverage']
    year_high = vix.info['fiftyTwoWeekHigh']
    year_low = vix.info['fiftyTwoWeekLow']

    vix_hist = vix.history(period='1mo')
    vix_close = vix_hist['Close'][-1]
    vix_lastweek_close = vix_hist['Close'][-7]
    vix_weekly_change = (vix_close - vix_lastweek_close)/vix_lastweek_close * 100

    print(
    f'''
    Welcome back.
    Previous close for VIX was {vix_close},
    and its weekly change is {np.round(vix_weekly_change ,3)}%.
        
    '''
    )