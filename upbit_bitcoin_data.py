import requests
import pandas as pd
import time

def fetch_upbit_btc_history():
    url = "https://api.upbit.com/v1/candles/days"
    headers = {"Accept": "application/json"}
    params = {
        "market": "KRW-BTC",
        "count": 200  # 최대 200개의 데이터를 한번에 가져올 수 있습니다.
    }
    all_data = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if not data:
            break

        all_data.extend(data)

        # 마지막 데이터의 날짜를 가져와서 그 이전 데이터를 가져오도록 설정
        last_date = data[-1]['candle_date_time_utc']
        params['to'] = last_date

        # API rate limit을 피하기 위해 잠시 대기
        time.sleep(0.1)

    df = pd.DataFrame(all_data)
    df['candle_date_time_utc'] = pd.to_datetime(df['candle_date_time_utc'])
    df = df.sort_values(by='candle_date_time_utc').reset_index(drop=True)

    # 필요한 컬럼만 선택
    df = df[['candle_date_time_utc', 'opening_price', 'high_price', 'low_price', 'trade_price', 'candle_acc_trade_volume']]

    return df

# 데이터 가져오기
btc_data = fetch_upbit_btc_history()

# 데이터 확인
print(btc_data.head())

# CSV로 저장
btc_data.to_csv('upbit_btc_history.csv', index=False)
