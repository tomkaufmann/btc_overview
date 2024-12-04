import datetime as dt
import streamlit as st
import pandas as pd
import mplfinance as mpf
import yfinance as yf

def get_data(symbol, start_date=None):
    df = yf.download(symbol, start=start_date, end=dt.datetime.now())
    for col in df.columns:
        df[col] = df[col].astype(float)
    df.index = pd.to_datetime(df.index)
    if start_date:
        df = df[df.index >= start_date]
    df.columns=[col[0] for col in df.columns]
    return df

st.set_page_config(page_title='BTC Overview', page_icon='favicon.ico')
st.title('BTC Overview')

c1, c2 = st.columns([1, 1])
with c1:
    sym = st.selectbox('Bitcoin or MicroStrategy', options=['Bitcoin', 'MicroStrategy'], index=0)
    if sym is 'Bitcoin':
        symbol='BTC-USD'
    else:
        symbol='MSTR'
with c2:
    date_from = st.date_input('Show data from', dt.datetime.now()-dt.timedelta(days=30))

st.markdown('---')

def plot_data(symbol, date_from, df):
    fig, ax = mpf.plot(
        df,
        title=f'{symbol}, {date_from}',
        type='candle',
        show_nontrading=True,
        mav=(int(30), int(200)),
        volume=True,
        style='yahoo',
        figsize=(15, 10),
        # Need this setting for Streamlit, see source code (line 778) here:
        # https://github.com/matplotlib/mplfinance/blob/master/src/mplfinance/plotting.py
        returnfig=True
    )
    st.pyplot(fig)

if symbol:
    df = get_data(symbol, str(date_from))
    plot_data(symbol, date_from, df)
