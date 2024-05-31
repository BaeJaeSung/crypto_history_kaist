import requests
import pandas as pd
import datetime
import time

def fetch_binance_btc_9am_history(start_date, end_date):
    url = "https://api.binance.com/api/v3/klines"
    current_date = start_date
    all_data = []
    current_year = start_date.year

    while current_date < end_date:
        start_9am = datetime.datetime(current_date.year, current_date.month, current_date.day, 9)
        end_10am = start_9am + datetime.timedelta(hours=1)
        start_timestamp = int(start_9am.timestamp() * 1000)
        end_timestamp = int(end_10am.timestamp() * 1000 - 1000)

        params = {
            'symbol': 'BTCUSDT',
            'interval': '1h',
            'startTime': start_timestamp,
            'endTime': end_timestamp
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data:
            for entry in data:
                entry_time = datetime.datetime.utcfromtimestamp(entry[0] / 1000)
                if entry_time.hour == 0:  # 오전 9시 데이터 필터링
                    all_data.append({
                        'Date': entry_time,
                        'Open': float(entry[1]),
                        'High': float(entry[2]),
                        'Low': float(entry[3]),
                        'Close': float(entry[4]),
                        'Volume': float(entry[5])
                    })
                    break  # 오전 9시의 첫 데이터만 필요하므로 루프 종료

        # 연도가 변경되면 데이터를 CSV 파일로 저장
        if current_date.year != current_year:
            df = pd.DataFrame(all_data)
            df.to_csv(f'binance_btc_daily_9am_history_{current_year}.csv', index=False)
            all_data = []  # 데이터 초기화
            current_year = current_date.year  # 현재 연도 업데이트

        current_date += datetime.timedelta(days=1)
        time.sleep(1)  # API rate limit을 피하기 위해 잠시 대기

    # 마지막 남은 데이터를 CSV 파일로 저장
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(f'binance_btc_daily_9am_history_{current_year}.csv', index=False)

    return pd.DataFrame(all_data)

# 2017년 9월 1일부터 현재까지의 데이터 가져오기
start_date = datetime.datetime(2019, 1, 1)
end_date = datetime.datetime(2020, 1, 2)

btc_binance_9am_data = fetch_binance_btc_9am_history(start_date, end_date)
print(btc_binance_9am_data.head())
