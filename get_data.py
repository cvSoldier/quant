import ccxt
import pandas as pd
import time

# 创建 Binance 交易所实例
exchange = ccxt.binance()

# 定义交易对和时间范围
symbol = 'OP/USDT'
timeframe = '5m'  # 5分钟的时间框架
since = exchange.parse8601('2023-01-01T00:00:00Z')  # 从2023年1月1日开始
end_timestamp = exchange.parse8601('2025-02-08T00:00:00Z')  # 结束时间

# 存储所有数据的列表
all_ohlcv = []

# 循环获取数据
while since < end_timestamp:
    print(f"Downloading data from {exchange.iso8601(since)}...")
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
    if not ohlcv:  # 如果没有数据，退出循环
        break
    all_ohlcv.extend(ohlcv)  # 将数据添加到列表
    since = ohlcv[-1][0] + 1  # 更新 since 为最后一根K线的时间戳 + 1 毫秒
    time.sleep(0.5)  # 避免请求频率过高

# 将数据转换为 Pandas DataFrame
df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# 将时间戳转换为日期时间格式
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# 设置时间戳为索引
df.set_index('timestamp', inplace=True)

# 保存为CSV文件
df.to_csv('OPUSDT_5m_full.csv')
print("Data saved to OPUSDT_5m_full.csv")