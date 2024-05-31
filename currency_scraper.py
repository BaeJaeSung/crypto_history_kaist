import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time

# 환율 정보를 스크래핑할 함수
def get_exchange_rate(date):
    url = f"https://www.x-rates.com/historical/?from=USD&amount=1&date={date}"  # x-rates.com의 URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # HTML 파싱하여 환율 데이터 추출
    table = soup.find('table', {'class': 'tablesorter ratesTable'})
    rate = None
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 2 and 'Korean Won' in cells[0].text:
            rate = cells[1].text
            break
    return float(rate.replace(',', '')) if rate else None

# 데이터 수집 시작 및 종료 날짜
start_date = datetime.date(2017, 1, 1)
end_date = datetime.date.today()

# 날짜 목록 생성
dates = pd.date_range(start_date, end_date, freq='D')

# 환율 데이터 저장할 리스트
exchange_rates = []

# 데이터 수집
for date in dates:
    try:
        rate = get_exchange_rate(date.strftime('%Y-%m-%d'))
        exchange_rates.append(rate)
        time.sleep(0.2)
        #print(exchange_rates)
    except Exception as e:
        print(f"Error fetching data for {date}: {e}")
        exchange_rates.append(None)

# 데이터프레임 생성
data = pd.DataFrame({
    'Date': dates,
    'USD_to_KRW': exchange_rates
})

# CSV 파일로 저장
csv_path = 'usd_to_krw_exchange_rates.csv'
data.to_csv(csv_path, index=False)
print(f"Data saved to {csv_path}")
