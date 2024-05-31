import pandas as pd

# CSV 파일 불러오기
ratio_df = pd.read_csv('data/upbit_divide_binance_ratio.csv')
usd_krw_df = pd.read_csv('data/usd_krw_investingcom.csv')

# 날짜 형식 변환
ratio_df['Date'] = pd.to_datetime(ratio_df['Date'])
usd_krw_df['Date'] = pd.to_datetime(usd_krw_df['Date'])

# 'ratio'와 'Open' 열의 데이터 형식 변환 (쉼표 제거 후 float 형식으로 변환)
ratio_df['ratio'] = ratio_df['ratio'].astype(float)
usd_krw_df['Open'] = usd_krw_df['Open'].str.replace(',', '').astype(float)

# 두 데이터프레임 병합 (inner join 사용)
merged_df = pd.merge(ratio_df, usd_krw_df, on='Date', how='inner')

# ratio / Open 계산
merged_df['kimchi_premium'] = merged_df['ratio'] / merged_df['Open'] - 1

# 결과를 CSV 파일로 저장
output_path = 'data/kimchi_premium.csv'
merged_df.to_csv(output_path, index=False)
