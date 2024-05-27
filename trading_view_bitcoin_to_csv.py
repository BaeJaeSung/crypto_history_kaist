from tvDatafeed import TvDatafeed, Interval
import pandas as pd

def fetch_tradingview_data():
    # TradingView에 로그인 정보가 없는 경우 guest 모드로 로그인
    tv = TvDatafeed()
    
    # 비트코인 데이터 가져오기
    symbol = 'BTCUSD'
    exchange = 'BITSTAMP'  # 데이터를 가져올 거래소를 지정
    start_date = '2011-09-01'
    
    data = tv.get_hist(symbol=symbol, exchange=exchange, interval=Interval.in_weekly, n_bars=10000)
    
    return data

def save_to_csv(df, filename='bitcoin_weekly_price.csv'):
    df.to_csv(filename, index=True)
    print(f"Data saved to {filename}")

def main():
    data = fetch_tradingview_data()
    data = data[data.index >= '2011-09-01']  # 2011년 9월 1일 이후의 데이터 필터링
    save_to_csv(data)

if __name__ == "__main__":
    main()
