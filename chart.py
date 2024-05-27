import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplfinance as mpf

# 임의의 데이터 생성
np.random.seed(0)
dates = pd.date_range(start="2024-01-01", periods=100, freq='D')
open_prices = np.random.normal(loc=30000, scale=800, size=100).round(2)
high_prices = open_prices + np.random.normal(loc=200, scale=50, size=100)
low_prices = open_prices - np.random.normal(loc=200, scale=50, size=100)
close_prices = open_prices + np.random.normal(loc=0, scale=100, size=100)
news_counts = np.random.poisson(lam=20, size=100)
narrative_dominant_factors = np.random.normal(loc=0.5, scale=0.1, size=100).round(2)
kimchi_premiums = np.random.normal(loc=0.05, scale=0.02, size=100).round(3)

# 데이터 프레임 생성
data = pd.DataFrame({
    "Date": dates,
    "Open": open_prices,
    "High": high_prices,
    "Low": low_prices,
    "Close": close_prices,
    "News Count": news_counts,
    "Narrative Dominant Factor": narrative_dominant_factors,
    "Kimchi Premium": kimchi_premiums
}).set_index('Date')

# 캔들스틱 차트와 추가 데이터를 표시하는 데 사용할 설정
apds = [mpf.make_addplot(data['News Count'], type='bar', ylabel='News Count', color='gray', secondary_y='auto'),
        mpf.make_addplot(data['Narrative Dominant Factor'], secondary_y='auto', color='green', ylabel='Narrative Factor'),
        mpf.make_addplot(data['Kimchi Premium'], secondary_y='auto', color='red', linestyle='--', ylabel='Kimchi Premium')]

# 캔들스틱 차트 그리기
mpf.plot(data[['Open', 'High', 'Low', 'Close']],
         type='candle',
         style='charles',
         title='Bitcoin Candlestick Chart with Additional Data',
         ylabel='Price ($)',
         addplot=apds,
         volume=False,
         figsize=(12, 8))
