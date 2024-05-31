import pandas as pd

# CSV 파일 불러오기
binance_df = pd.read_csv('data/binance_btc_9am_total.csv')
upbit_df = pd.read_csv('data/upbit_9am_filtered.csv')

# 날짜 형식 변환
binance_df['Date'] = pd.to_datetime(binance_df['Date'])
upbit_df['candle_date_time_utc'] = pd.to_datetime(upbit_df['candle_date_time_utc'])

# 각 데이터프레임에서 필요한 컬럼만 선택
binance_df = binance_df[['Date', 'Open']]
upbit_df = upbit_df[['candle_date_time_utc', 'opening_price']]

# 컬럼명 변경
binance_df.rename(columns={'Open': 'A'}, inplace=True)
upbit_df.rename(columns={'candle_date_time_utc': 'Date', 'opening_price': 'B'}, inplace=True)

# 두 데이터프레임 병합
merged_df = pd.merge(upbit_df, binance_df, on='Date')

# B/A 계산
merged_df['ratio'] = merged_df['B'] / merged_df['A']

# 결과를 CSV 파일로 저장
output_path = 'data/upbit_divide_binance_ratio.csv'
merged_df.to_csv(output_path, index=False)
