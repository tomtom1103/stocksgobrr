import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
from tqdm import tqdm
import yfinance as yf
import fear_and_greed
from datetime import datetime, timedelta
from pytz import timezone
import pyautogui as pg
import guicoordinates as coord
import time

class Autolog:

    def __init__(self):
        self.now = datetime.now()

    def daily(self):
        vix = yf.Ticker(f"^VIX")
        vix_fifty_day_avg = vix.info['fiftyDayAverage']
        vix_twohundred_day_avg = vix.info['twoHundredDayAverage']

        vix_hist = vix.history(period='1mo')
        vix_close = vix_hist['Close'][-1]
        vix_lastweek_close = vix_hist['Close'][-7]
        vix_threeday_close = vix_hist['Close'][-3]
        vix_weekly_change = (vix_close - vix_lastweek_close) / vix_lastweek_close * 100
        vix_threeday_change = (vix_close - vix_threeday_close) / vix_threeday_close * 100

        dow = yf.Ticker(f"^DJI")
        dow_hist = dow.history(period='1mo')
        dow_close = dow_hist['Close'][-1]
        dow_lastweek_close = dow_hist['Close'][-7]
        dow_threeday_close = dow_hist['Close'][-3]
        dow_weekly_change = (dow_close - dow_lastweek_close) / dow_lastweek_close * 100
        dow_threeday_change = (dow_close - dow_threeday_close) / dow_threeday_close * 100

        snp = yf.Ticker('^GSPC')
        snp_hist = snp.history(period='1mo')
        snp_close = snp_hist['Close'][-1]
        snp_lastweek_close = snp_hist['Close'][-7]
        snp_threeday_close = snp_hist['Close'][-3]
        snp_weekly_change = (snp_close - snp_lastweek_close) / snp_lastweek_close * 100
        snp_threeday_change = (snp_close - snp_threeday_close) / snp_threeday_close * 100

        nasdaq = yf.Ticker('^IXIC')
        nasdaq_hist = nasdaq.history(period='1mo')
        nasdaq_close = nasdaq_hist['Close'][-1]
        nasdaq_lastweek_close = nasdaq_hist['Close'][-7]
        nasdaq_threeday_close = nasdaq_hist['Close'][-3]
        nasdaq_weekly_change = (nasdaq_close - nasdaq_lastweek_close) / nasdaq_lastweek_close * 100
        nasdaq_threeday_change = (nasdaq_close - nasdaq_threeday_close) / nasdaq_threeday_close * 100

        fng = fear_and_greed.get()
        fng_value = fng[0]
        fng_sentiment = fng[1]
        fng_date = fng[2]

        recap = (
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
        print(recap) #for the terminal
        return recap #for bear

    def particularstock_stockinfo(self, ticker):
        company = yf.Ticker(f"{ticker}")
        company_name = company.info['longName']
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

    def particularstock_earnings(self, ticker):
        kst = timezone('Asia/Seoul')
        es = timezone('US/Eastern')
        next_earnings = si.get_next_earnings_date(ticker)
        next_earnings = es.localize(next_earnings)
        local_next_earnings = next_earnings.astimezone(kst)

        print(
            f'''
        {ticker} will release their next earnings on
        {next_earnings}, Eastern Time, or
        {local_next_earnings}, Korean Standard Time.
        
        
        {self.now}
            '''
        )

    def mystocks_stocklist(self):
        mystocks = pd.read_excel('mystocks.xlsx')
        mystocklist = mystocks['My Stocks'].tolist()
        print(mystocklist)

    def mystocks_twohundred(self):
        mystocks = pd.read_excel('mystocks.xlsx')
        mystocklist = mystocks['My Stocks']
        count = 0
        print(
            f'''
        ------------------------------
        You currently own {mystocklist.size} stocks. Assessing 200 day average..
        ------------------------------
            ''')

        for ticker in mystocklist:
            company = yf.Ticker(f"{ticker}")
            company_name = company.info['longName']
            twohundred_day_avg = company.info['twoHundredDayAverage']
            company_hist = company.history(period='1mo')
            company_close = np.round(company_hist['Close'][-1])

            if company_close < twohundred_day_avg:
                count += 1
                print(
                    f'''
        {company_name}'s current price is below the 200 day average.

        Purchasing price: ${float(mystocks.loc[mystocks['My Stocks'] == f'{ticker}']['PP'])}
        200 day avg: ${twohundred_day_avg}
        Current price: ${company_close}
        ------------------------------
                '''
                )

            else:
                print(
                    f'''
        everything looks good for {company_name}.
        ------------------------------ 
                ''')

        print(
            f'''
        ------------------------------
        {count} stocks are below the 200 day average line.
        ------------------------------
            '''
        )

    def news(self, ticker):
        pass


    """
    Menu Starts Here.
    """

    def main_menu(self):
        choice = int(input(
        """
        ------------Main Menu------------
                                         |   
        What Menu would you like to see? |   
        1. Particular stock              |   
        2. My stocks                     |   
        3. News #NOTYET                  |     
        4. Log to Bear                   |   
                                         |   
        ------------Main Menu------------
        >> """

        ))

        if choice == 1:
            ticker = input("Input ticker>> ")
            thomas.particularstock_menu(ticker)
        elif choice == 2:
            thomas.mystocks_menu()
        elif choice == 3:
            print('notyet')
            thomas.main_menu()
        elif choice == 4:
            thomas.bear_menu()


    def mystocks_menu(self):
        choice = int(input(
        """
        ------------My Stocks------------
                                         |
        What Menu would you like to see? |
        1. My Stock List                 |
        2. 200 Day Assessment            |
        3. News #NOTYET                  |
        4. Back to Main Menu             |
                                         |
        ------------My Stocks------------
        >> """

        ))

        if choice == 1:
            thomas.mystocks_stocklist()
            thomas.mystocks_menu()
        elif choice == 2:
            thomas.mystocks_twohundred()
            thomas.mystocks_menu()
        elif choice == 3:
            print('notyet')
            thomas.mystocks_menu()
        elif choice == 4:
            thomas.main_menu()

    def particularstock_menu(self,ticker):

        choice = int(input(
        """
        ------------Particular Stock------------
                                         |
        What Menu would you like to see? |
        1. Stock Info                    |
        2. Earnings Info                 |
        3.                               |
        4. Back to Main Menu             |
                                         |
        ------------Particular Stock------------
        >> """

        ))

        if choice == 1:
            thomas.particularstock_stockinfo(ticker)
            thomas.particularstock_menu(ticker)
        elif choice == 2:
            thomas.particularstock_earnings(ticker)
            thomas.particularstock_menu(ticker)
        elif choice == 3:
            pass
        elif choice == 4:
            thomas.main_menu()

    def bear_menu(self):
        choice = int(input(
        """
        ------------Bear Notes------------
                                         |
        What would you like to do?       |
        1. Initialize Bear               |
        2. Log today's recap             |
        3. Back to Main Menu             |
                                         |
        ------------Bear Notes------------
        >> """
        ))

        if choice == 1:
            thomas.bear_init()
            thomas.bear_menu()

        elif choice == 2:
            thomas.bear_log()
            thomas.bear_menu()
        elif choice == 3:
            thomas.main_menu()


    def bear_init(self):
        dt = datetime.today()
        month = dt.strftime('%B')
        day = dt.strftime('%-d')
        weekday = dt.strftime('%A')

        pg.click(x=coord.test_x, y=coord.test_y) #임시 bear clicker
        time.sleep(0.5)
        pg.click(x=coord.stock_x, y=coord.stock_y) #투자메뉴
        time.sleep(0.5)
        pg.click(x=coord.newnote_x, y=coord.newnote_y) #새로운 노트
        time.sleep(0.5)

        pg.typewrite(f'{month} {day} - {weekday}')
        time.sleep(0.5)
        pg.press(['down', 'enter', 'enter'],interval=0.1)

    def bear_log(self):
        time.sleep(0.5)
        pg.click(x=500, y=432)
        pg.write(f'{daily}')



if __name__ == '__main__':
    print("running autolog...")

    thomas = Autolog()
    daily = thomas.daily()
    thomas.main_menu()
