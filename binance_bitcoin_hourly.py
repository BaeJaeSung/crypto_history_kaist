import requests
import pandas as pd
import datetime
import time

def fetch_binance_btc_hourly_history(start_date, end_date):
    url = "https://api.binance.com/api/v3/klines"
    start_timestamp = int(start_date.timestamp() * 1000)
    end_timestamp = int(end_date.timestamp() * 1000)
    
    all_data = []
    
    while start_timestamp < end_timestamp:
        params = {
            'symbol': 'BTCUSDT',
            'interval': '1h',
            'startTime': start_timestamp,
            'endTime': min(start_timestamp + 60000 * 1000, end_timestamp)  # 최대 1000개의 데이터를 한번에 가져옴
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if not data:
            break
        
        for entry in data:
            all_data.append({
                'Date': datetime.datetime.utcfromtimestamp(entry[0] / 1000),
                'Open': float(entry[1]),
                'High': float(entry[2]),
                'Low': float(entry[3]),
                'Close': float(entry[4]),
                'Volume': float(entry[5])
            })
        
        # 다음 타임스탬프로 이동 (마지막 데이터의 타임스탬프 + 1밀리초)
        start_timestamp = data[-1][0] + 1
        
        # API rate limit을 피하기 위해 잠시 대기
        time.sleep(1)
    
    return pd.DataFrame(all_data)

# 2017년 9월 1일부터 현재까지의 데이터 가져오기
dates = [[2017,9,1], [2018,1,1], [2018,5,1], [2018,9,1], [2019,1,1], [2019,5,1], [2019,9,1], [2020,1,1], [2020,5,1], [2020,9,1], [2021,1,1], [2021,5,1], [2021,9,1], [2022,1,1], [2022,5,1], [2022,9,1], [2023,1,1], [2023,5,1], [2023,9,1], [2024,1,1], [2024,5,1]]
for date in dates:
    start_date = datetime.datetime(date[0], date[1], date[2])
    end_date = datetime.datetime.now()
    btc_binance_hourly_data = fetch_binance_btc_hourly_history(start_date, end_date)
    print(btc_binance_hourly_data.head())
    btc_binance_hourly_data.to_csv(f'binance_btc_hourly_history_{date[0]}_{date[1]}_{date[2]}.csv', index=False)
