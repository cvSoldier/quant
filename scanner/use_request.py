import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

IS_TEST = False
def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        # print(f"{func.__name__} finished in {end_time - start_time:.6f} seconds.")

        return result

    return wrapper


def convert_to_beijing_time(df):
    """
    将时间列转换为北京时间。
    Yahoo Finance 返回的时间是 UTC-5 时间，北京时间是 UTC+8。
    
    :param df: 包含时间列的 DataFrame
    :return: 转换后的 DataFrame
    """
    if not df.empty:
        # 将时间列转换为 DatetimeIndex（如果尚未转换）
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        
        # 将 UTC 时间转换为北京时间（UTC+8）
        df.index = df.index + timedelta(hours=13)
    
    return df

def save_to_csv(data, filename):
    """
    将数据保存到 CSV 文件。
    
    :param data: 要保存的 DataFrame
    :param filename: 保存的文件名
    """
    try:
        data.to_csv(filename, encoding='utf-8-sig')  # 使用 utf-8-sig 编码避免中文乱码
        print(f"数据已保存到 {filename}")
    except Exception as e:
        print(f"保存数据失败: {e}")


def save_last_20_min_data(list_rows, stock_list):
    for row in list_rows:
        try:
            # 提取股票代码
            ticker = row.find('a', class_='tickerName-GrtoTeat').text.strip()
            # 提取涨幅
            change = row.find('span', class_='positive-p_QIAEOQ').text.strip()
            change = float(change[1:-1])
            if change > 10:
                stock_list.append(ticker)
            # # 提取价格
            # price_cell = row.find_all('td', class_='cell-RLhfr_y4 right-RLhfr_y4')[1]  # 第二个符合条件的<td>
            # price = float(price_cell.text.strip().split()[0])
            # vol_cel = row.find_all('td', class_='cell-RLhfr_y4 right-RLhfr_y4')[2]
            # vol_txt = vol_cel.text.encode('utf-8').replace(b'\xe2\x80\xaf', b'').decode('utf-8')
            # if 'K' in vol_txt:
            #     volume = float(vol_txt.replace('K', '')) * 1e3
            # elif 'M' in vol_txt:
            #     volume = float(vol_txt.replace('M', '')) * 1e6
            # else:
            #     volume = float(vol_txt)
            # td_all = row.find_all('td', class_='cell-RLhfr_y4 right-RLhfr_y4')

            # print(td_all)
            # print(f"股票代码: {ticker}, 涨幅: {change}%, 价格: {price}")
        except Exception as e:
            # 如果某个元素未找到，跳过该行
            # print(f"解析失败: {e}")
            continue

def get_request(is_pre, stock_list):
    # 目标URL
    PREV_URL = 'https://cn.tradingview.com/markets/stocks-usa/market-movers-pre-market-gainers/'
    URL = 'https://cn.tradingview.com/markets/stocks-usa/market-movers-gainers/'
    url = PREV_URL if is_pre else URL
    Cookie = '__eoi=ID=240fa7f019267950:T=1740316804:RT=1740316804:S=AA-AfjbJp4H6baKAFJLYgth0Fbct;__gads=ID=e3d5adff96d0e7b4:T=1740316804:RT=1740316804:S=ALNI_MaAmyI4r-yviDtc506P4aWLFEsjJQ;__gpi=UID=00001048cbf5bdd0:T=1740316804:RT=1740316804:S=ALNI_MbIr5Z5Kmw6Qw8G7MAjrp4MWyMcbA;_ga=GA1.1.1233108505.1738595349;_ga_YVVRYGL0E0=GS1.1.1741352370.39.1.1741353180.58.0.0;_sp_id.cf1a=417e44ab-7e61-4e3e-9886-7b243d437dfc.1731934501.21.1741353180.1741271899.8a8fc797-8bd2-46e0-a400-b2b30eefb8c9.f72d2d44-f6e9-4b91-847b-f81ed81dd724.bcbdc5c7-bf54-40c2-b019-cb6805560687.1741352892554.3;_sp_ses.cf1a=*;cachec=3f045c69-fd72-42a7-95d3-924c2cc6b302;cookiePrivacyPreferenceBannerProduction=accepted;cookiesSettings={"analytics":true,"advertising":true};device_t=VDYxeUJROjIsb2RGa0JROjMsREptZEJROjE.7jsVyj-98b8JeONequwC9Gw_BJDEXTEIedMB37MAWVk;etg=3f045c69-fd72-42a7-95d3-924c2cc6b302;png=3f045c69-fd72-42a7-95d3-924c2cc6b302;sessionid=6ldhwhjneb6nn2sl1a2lk01zglv55t34;sessionid_sign=v3:lEoqyYNitbAlvrJrzGd6cYHCXq6j5AJUkZzcrkQTtUw=;theme=light;tv_ecuid=3f045c69-fd72-42a7-95d3-924c2cc6b302;'
    headers = {
        'Cookie': Cookie
    }
    # 发送HTTP请求
    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有class包含'listRow'的元素
        list_rows = soup.find_all(class_='listRow')
        save_last_20_min_data(list_rows, stock_list)

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

if __name__ == '__main__':
    get_request(False)