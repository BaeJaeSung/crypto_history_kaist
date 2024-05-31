import pandas as pd

# CSV 파일 불러오기
upbit_df = pd.read_csv('data/upbit_btc_hourly_history.csv')

# 날짜 형식 변환
upbit_df['candle_date_time_utc'] = pd.to_datetime(upbit_df['candle_date_time_utc'])

# 9:00 AM의 데이터 필터링
upbit_9am = upbit_df[upbit_df['candle_date_time_utc'].dt.hour == 9].copy()

# 결과를 CSV 파일로 저장
output_path = 'data/upbit_9am_filtered.csv'
upbit_9am.to_csv(output_path, index=False)
