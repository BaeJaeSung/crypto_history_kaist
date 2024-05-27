import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num
from matplotlib.animation import FuncAnimation
from mplfinance.original_flavor import candlestick_ohlc

# 데이터 로드
file_path = 'data/trading_view_data_feed.csv'
df = pd.read_csv(file_path)
show_frame = 180  # 한 번에 표시할 캔들 개수

# datetime 컬럼을 datetime 형식으로 변환
df['datetime'] = pd.to_datetime(df['datetime'])

# 필요한 컬럼만 선택
df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]

# 캔들 차트를 그리기 위해 필요한 형식으로 데이터 변환
df['date_num'] = date2num(df['datetime'])

# 메모 데이터 로드
memo1_file_path = 'data/memo1.csv'
memo2_file_path = 'data/memo2.csv'

memo1 = pd.read_csv(memo1_file_path)
memo2 = pd.read_csv(memo2_file_path)

# datetime 형식 변환
memo1['datetime'] = pd.to_datetime(memo1['datetime'])
memo2['start_date'] = pd.to_datetime(memo2['start_date'])
memo2['end_date'] = pd.to_datetime(memo2['end_date'])

# 초기 설정
fig, ax = plt.subplots()

def plot_candlestick(data):
    ohlc = data[['date_num', 'open', 'high', 'low', 'close']].copy()
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='g', colordown='r', alpha=0.8)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

def update(frame):
    ax.clear()
    start = frame
    end = frame + show_frame
    candlestick_data = df.iloc[start:end]
    plot_candlestick(candlestick_data)
    
    # 메모1 표시 (화살표 없음)
    ylim = ax.get_ylim()
    for i, row in memo1.iterrows():
        if row['datetime'] in candlestick_data['datetime'].values:
            ax.annotate(row['memo'], 
                        (date2num(row['datetime']), ylim[1]),  # y 위치를 ylim[1]으로 설정
                        xytext=(40, -(30 + 20 * (i % 2))), textcoords='offset points',
                        fontsize=20,  # 텍스트 크기 설정
                        ha='center', va='top')
    
    # 메모2 표시 (영역)
    for i, row in memo2.iterrows():
        if row['start_date'] <= candlestick_data['datetime'].iloc[-1] and row['end_date'] >= candlestick_data['datetime'].iloc[0]:
            start_num = max(date2num(row['start_date']), candlestick_data['date_num'].iloc[0])
            end_num = min(date2num(row['end_date']), candlestick_data['date_num'].iloc[-1])
            ax.axvspan(start_num, end_num, color=row['color'], alpha=0.3)
    
    ax.set_title(f'{candlestick_data["datetime"].iloc[0].date()} to {candlestick_data["datetime"].iloc[-1].date()}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.grid(True)

# 초기 캔들 차트 생성
plot_candlestick(df.iloc[:show_frame])

# 애니메이션 설정
ani = FuncAnimation(fig, update, frames=range(len(df) - show_frame), interval=20, repeat=False)

plt.show()