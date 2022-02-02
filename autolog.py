#import pandas as pd
import numpy as np
#from yahoo_fin import stock_info as si
#from tqdm import tqdm
import yfinance as yf

class Autolog:

    def __init__(self):
        pass


    def daily(self, ticker):
        company = yf.Ticker(f"{ticker}")
        fifty_day_avg = company.info['fiftyDayAverage']
        twohundred_day_avg = company.info['twoHundredDayAverage']
        year_high = company.info['fiftyTwoWeekHigh']
        year_low = company.info['fiftyTwoWeekLow']

        company_hist = company.history(period='1mo')
        company_close = company_hist['Close'][-1]
        company_lastweek_close = company_hist['Close'][-7]
        company_weekly_change = (company_close - company_lastweek_close)/company_lastweek_close * 100


        print(
            f'''
        Welcome back Tom.
        Previous close for {ticker} was {np.round(company_close, 3)},
        and its weekly change is {np.round(company_weekly_change, 3)}%.
        50-day average: {fifty_day_avg}
        200-day average: {twohundred_day_avg}. 
        '''
        )

    def stockinfo(self, ticker):
        company = yf.Ticker(f"{ticker}")
        fifty_day_avg = company.info['fiftyDayAverage']
        twohundred_day_avg = company.info['twoHundredDayAverage']
        year_high = company.info['fiftyTwoWeekHigh']
        year_low = company.info['fiftyTwoWeekLow']

        company_hist = company.history(period='1mo')
        company_close = company_hist['Close'][-1]
        company_lastweek_close = company_hist['Close'][-7]
        company_weekly_change = (company_close - company_lastweek_close)/company_lastweek_close * 100


        print(
            f'''
        Previous close for {ticker} was ${np.round(company_close, 3)},
        and its weekly change is {np.round(company_weekly_change, 3)}%.
        50-day average: ${fifty_day_avg}
        200-day average: ${twohundred_day_avg}. 
        '''
        )



if __name__ == '__main__':
    print("running autolog...")

    today = Autolog()
    today.daily("^VIX")
    stock = Autolog()
    ticker = input("Input ticker>> ")
    stock.stockinfo(ticker)