import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
import pickle


def tickers():
    df1 = pd.DataFrame(si.tickers_sp500())
    df2 = pd.DataFrame(si.tickers_nasdaq())
    df3 = pd.DataFrame(si.tickers_dow())
    df4 = pd.DataFrame(si.tickers_other())

    sym1 = set(symbol for symbol in df1[0].values.tolist())
    sym2 = set(symbol for symbol in df2[0].values.tolist())
    sym3 = set(symbol for symbol in df3[0].values.tolist())
    sym4 = set(symbol for symbol in df4[0].values.tolist())

    symbols = set.union(sym1, sym2, sym3, sym4)

    my_list = ['W', 'R', 'P', 'Q']  # warrants, rights, first preferred issue, bankruptcy
    del_set = set()
    sav_set = set()

    for symbol in symbols:
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
    tickers.to_pickle('utils/tickers.pkl')


if __name__ == '__main__':
    tickers()
