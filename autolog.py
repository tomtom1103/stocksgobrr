#import pandas as pd
import numpy as np
#from yahoo_fin import stock_info as si
#from tqdm import tqdm
import yfinance as yf

class Autolog:

    def __init__(self):
        pass


    def daily(self):
        vix = yf.Ticker(f"^VIX")
        vix_fifty_day_avg = vix.info['fiftyDayAverage']
        vix_twohundred_day_avg = vix.info['twoHundredDayAverage']

        vix_hist = vix.history(period='1mo')
        vix_close = vix_hist['Close'][-1]
        vix_lastweek_close = vix_hist['Close'][-7]
        vix_weekly_change = (vix_close - vix_lastweek_close)/vix_lastweek_close * 100

        dow = yf.Ticker(f"^DJI")
        dow_hist = dow.history(period='1mo')
        dow_close = dow_hist['Close'][-1]
        dow_lastweek_close = dow_hist['Close'][-7]
        dow_weekly_change = (dow_close - dow_lastweek_close)/dow_lastweek_close * 100

        snp = yf.Ticker('^GSPC')
        snp_hist = snp.history(period='1mo')
        snp_close = snp_hist['Close'][-1]
        snp_lastweek_close = snp_hist['Close'][-7]
        snp_weekly_change = (snp_close - snp_lastweek_close)/snp_lastweek_close * 100

        nasdaq = yf.Ticker('^IXIC')
        nasdaq_hist = nasdaq.history(period='1mo')
        nasdaq_close = nasdaq_hist['Close'][-1]
        nasdaq_lastweek_close = nasdaq_hist['Close'][-7]
        nasdaq_weekly_change = (nasdaq_close - nasdaq_lastweek_close)/nasdaq_lastweek_close * 100

        print(
            f'''
        Welcome back Tom.
        Previous close for VIX was {np.round(vix_close, 3)},
        and its weekly change is {np.round(vix_weekly_change, 3)} %.
        50-day average: {vix_fifty_day_avg}, 200-day average: {vix_twohundred_day_avg}.
        
        Weekly Change recap
        Dow Jones: {np.round(dow_weekly_change, 3)} %
        S&P 500: {np.round(snp_weekly_change, 3)} %
        NASDAQ: {np.round(nasdaq_weekly_change, 3)} %
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
    today.daily()
    stock = Autolog()
    ticker = input("Input ticker>> ")
    stock.stockinfo(ticker)