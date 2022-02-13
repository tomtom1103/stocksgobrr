import pandas as pd
import numpy as np
#from yahoo_fin import stock_info as si
#from tqdm import tqdm
import yfinance as yf
import fear_and_greed

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
        vix_threeday_close = vix_hist['Close'][-3]
        vix_weekly_change = (vix_close - vix_lastweek_close)/vix_lastweek_close * 100
        vix_threeday_change = (vix_close - vix_threeday_close)/vix_threeday_close * 100

        dow = yf.Ticker(f"^DJI")
        dow_hist = dow.history(period='1mo')
        dow_close = dow_hist['Close'][-1]
        dow_lastweek_close = dow_hist['Close'][-7]
        dow_threeday_close = dow_hist['Close'][-3]
        dow_weekly_change = (dow_close - dow_lastweek_close)/dow_lastweek_close * 100
        dow_threeday_change = (dow_close - dow_threeday_close)/dow_threeday_close * 100

        snp = yf.Ticker('^GSPC')
        snp_hist = snp.history(period='1mo')
        snp_close = snp_hist['Close'][-1]
        snp_lastweek_close = snp_hist['Close'][-7]
        snp_threeday_close = snp_hist['Close'][-3]
        snp_weekly_change = (snp_close - snp_lastweek_close)/snp_lastweek_close * 100
        snp_threeday_change = (snp_close - snp_threeday_close)/snp_threeday_close * 100

        nasdaq = yf.Ticker('^IXIC')
        nasdaq_hist = nasdaq.history(period='1mo')
        nasdaq_close = nasdaq_hist['Close'][-1]
        nasdaq_lastweek_close = nasdaq_hist['Close'][-7]
        nasdaq_threeday_close = nasdaq_hist['Close'][-3]
        nasdaq_weekly_change = (nasdaq_close - nasdaq_lastweek_close)/nasdaq_lastweek_close * 100
        nasdaq_threeday_change = (nasdaq_close - nasdaq_threeday_close)/nasdaq_threeday_close * 100

        fng = fear_and_greed.get()
        fng_value = fng[0]
        fng_sentiment = fng[1]
        fng_date = fng[2]

        print(
            f'''
        ----------RECAP----------
        Welcome back Tom.
        Previous close for VIX was {np.round(vix_close, 3)},
        VIX weekly change is {np.round(vix_weekly_change, 3)} %.
        VIX three day change is {np.round(vix_threeday_change, 3)} %.
        50-day average: {vix_fifty_day_avg}, 200-day average: {vix_twohundred_day_avg}.
        
        Fear and Greed Index
        Current market sentiment is at {fng_value}, {fng_sentiment}.
        last indexed at {fng_date}.
        
        Three day change recap
        Dow Jones: {np.round(dow_threeday_change, 3)} %
        S&P 500: {np.round(snp_threeday_change, 3)} %
        NASDAQ: {np.round(nasdaq_threeday_change, 3)} %
        
        Weekly Change recap
        Dow Jones: {np.round(dow_weekly_change, 3)} %
        S&P 500: {np.round(snp_weekly_change, 3)} %
        NASDAQ: {np.round(nasdaq_weekly_change, 3)} %
        ----------RECAP----------
        '''
        )

    def stockinfo(self, ticker):
        company = yf.Ticker(f"{ticker}")
        company_name = company.info['shortName']
        fifty_day_avg = company.info['fiftyDayAverage']
        twohundred_day_avg = company.info['twoHundredDayAverage']
        year_high = company.info['fiftyTwoWeekHigh']
        year_low = company.info['fiftyTwoWeekLow']

        company_hist = company.history(period='1mo')
        company_close = company_hist['Close'][-1]
        company_lastweek_close = company_hist['Close'][-7]
        company_threeday_close = company_hist['Close'][-3]
        company_weekly_change = (company_close - company_lastweek_close)/company_lastweek_close * 100
        company_threeday_change = (company_close - company_threeday_close)/company_threeday_close * 100


        print(
            f'''
        ----------{company_name}----------
        
        Previous close for {company_name} was ${np.round(company_close, 3)},
        Its weekly change is {np.round(company_weekly_change, 3)} %.
        Its three day change is {np.round(company_threeday_change, 3)} %.
        50-day average: ${fifty_day_avg}
        200-day average: ${twohundred_day_avg}.
        
        ----------{company_name}----------    
        '''
        )

    def mystocks(self):
        mystocks = pd.read_excel('mystocks.xlsx')
        mystocklist = mystocks['My Stocks'].tolist()

        for ticker in mystocklist:
            thomas.stockinfo(ticker)
            '''
            company = yf.Ticker(f"{ticker}")
            company_name = company.info['shortName']
            fifty_day_avg = company.info['fiftyDayAverage']
            twohundred_day_avg = company.info['twoHundredDayAverage']
            year_high = company.info['fiftyTwoWeekHigh']
            year_low = company.info['fiftyTwoWeekLow']

            company_hist = company.history(period='1mo')
            company_close = company_hist['Close'][-1]
            company_lastweek_close = company_hist['Close'][-7]
            company_threeday_close = company_hist['Close'][-3]
            company_weekly_change = (company_close - company_lastweek_close) / company_lastweek_close * 100
            company_threeday_change = (company_close - company_threeday_close) / company_threeday_close * 100
            '''
        #print(mystocks)

    def news(self,ticker):
        pass


    def flowcontrol(self):
        choice = int(input(
        """
        --------------------------------
        
        What Menu would you like to see?
        1. Particular stock
        2. My stocks
        3. News
        
        --------------------------------
        >> """

        ))

        if choice == 1:
            ticker = input("Input ticker>> ")
            thomas.stockinfo(ticker)
            thomas.flowcontrol()
        elif choice == 2:
            thomas.mystocks()
            thomas.flowcontrol()


if __name__ == '__main__':
    print("running autolog...")

    thomas = Autolog()
    thomas.daily()
    thomas.flowcontrol()
