import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
from tqdm import tqdm
import pickle

sp500 = pd.DataFrame(si.tickers_sp500())
nasdaq = pd.DataFrame(si.tickers_nasdaq())
dow = pd.DataFrame(si.tickers_dow())
other = pd.DataFrame(si.tickers_other())
kws = pd.DataFrame(['SPY', 'VTI', 'HODL', 'ATH'])

sym1 = set(symbol for symbol in sp500[0].values.tolist())
sym2 = set(symbol for symbol in nasdaq[0].values.tolist())
sym3 = set(symbol for symbol in dow[0].values.tolist())
sym4 = set(symbol for symbol in other[0].values.tolist())
sym5 = set(symbol for symbol in kws[0].values.tolist())

def tickers(*args):
    symbols = set.union(*args)

    my_list = ['W', 'R', 'P', 'Q']  # warrants, rights, first preferred issue, bankruptcy
    del_set = set()
    sav_set = set()

    for symbol in tqdm(symbols):
        if len(symbol) > 4 and symbol[-1] in my_list:
            del_set.add(symbol)
        else:
            sav_set.add(symbol)

    sav_set = list(sav_set)
    tickers = pd.DataFrame(sav_set)
    tickers['tickers'] = tickers[0]
    del tickers[0]

    if (tickers['tickers'].str.len() < 1).sum():
        tickers['tickers'].replace('', np.nan, inplace=True)
        tickers.dropna(subset=['tickers'], inplace=True)
    else:
        pass

    tickers['length'] = tickers.tickers.str.len()
    tickers = tickers[tickers.length > 1] #한글자 티커는 드랍

    tickers = tickers[~tickers.tickers.str.contains('PY')]
    tickers = tickers[~tickers.tickers.str.contains('ST')]
    tickers = tickers[~tickers.tickers.str.contains('TH')]
    #진짜 개무식한 코드. 나중에 바꾸자

    tickers.to_pickle('utils/tickers_big3.pkl')
    print('done')


if __name__ == '__main__':
    tickers(sym1,sym2,sym3,sym5)
