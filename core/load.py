from core import *

def get_data():
    """
    The function should load all data into a db and from there the web app should read the data. In this way the time
    required to load the page should drop significantly. A job should be executed every day to drop the tables and load
    the new data
    :return:
    """
    stock_indices = ['^GSPC', '^IXIC', '^DJI', '^FTSE', '^GDAXI', '^N225', 'FTSEMIB.MI']
    currency_pairs = ['EUR=X', 'GBP=X', 'JPY=X', 'CHF=X', 'CAD=X', 'AUD=X']

    # retrive data
    web = True
    if web:
        calend = economic_calendar()
        gy = yield_rate("germany")
        uy = yield_rate("united-kingdom")
        iy = yield_rate("italy")
        usy = yield_rate("united-states")
        ii = get_inflation("italy-inflation-rate")
        ei = get_inflation("euro-area-historical-inflation-rate")
        usi = get_inflation("usa-inflation-rate")
        euribor = Euribor()
        GDP = GDP_g20().iloc[:11]

    pd_st = []
    for i in stock_indices:
        f = yf.Ticker(i)
        df = f.history(period='1y')
        df['EMA20'] = df['Close'].ewm(span=20).mean()
        df['EMA50'] = df['Close'].ewm(span=50).mean()
        sign = ['']
        for i in range(1, len(df)):
            if df['EMA20'].iloc[i] > df['EMA50'].iloc[i] and df['EMA20'].iloc[i - 1] <= df['EMA50'].iloc[i - 1]:
                sign.append("^")
            elif df['EMA20'].iloc[i] < df['EMA50'].iloc[i] and df['EMA20'].iloc[i - 1] >= df['EMA50'].iloc[i - 1]:
                sign.append("v")
            else:
                sign.append("")
        df['sign'] = sign
        pd_st.append(df[-31:-1])

    pd_cp = []
    for i in currency_pairs:
        f = yf.Ticker(i)
        df = f.history(period='1y')
        df['EMA20'] = df['Close'].ewm(span=20).mean()
        df['EMA50'] = df['Close'].ewm(span=50).mean()
        sign = ['']
        for i in range(1, len(df)):
            if df['EMA20'].iloc[i] > df['EMA50'].iloc[i] and df['EMA20'].iloc[i - 1] <= df['EMA50'].iloc[i - 1]:
                sign.append("^")
            elif df['EMA20'].iloc[i] < df['EMA50'].iloc[i] and df['EMA20'].iloc[i - 1] >= df['EMA50'].iloc[i - 1]:
                sign.append("v")
            else:
                sign.append("")
        df['sign'] = sign
        pd_cp.append(df.iloc[-41:-1])

    return 0


