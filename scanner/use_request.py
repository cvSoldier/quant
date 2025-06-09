import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time


def save_last_20_min_data(is_pre, list_rows, stock_list):
    for row in list_rows:
        try:
            # 提取股票代码
            ticker = row.find('a', class_='tickerName-GrtoTeat').text.strip()
            # 提取涨幅
            change = row.find('span', class_='positive-p_QIAEOQ').text.strip()
            change = float(change[1:-1])
            # 提取价格
            price_cell = row.find_all('td', class_='cell-RLhfr_y4 right-RLhfr_y4')[1]  # 第二个符合条件的<td>
            price = float(price_cell.text.strip().split()[0])
            
            vol_index = 3 if is_pre else 2
            vol_cel = row.find_all('td', class_='cell-RLhfr_y4 right-RLhfr_y4')[vol_index]
            vol_txt = vol_cel.text.encode('utf-8').replace(b'\xe2\x80\xaf', b'').decode('utf-8')
            td_all = row.find_all('td', class_='cell-RLhfr_y4 right-RLhfr_y4')
            if 'K' in vol_txt:
                volume = float(vol_txt.replace('K', '')) * 1e3
            elif 'M' in vol_txt:
                volume = float(vol_txt.replace('M', '')) * 1e6
            else:
                volume = float(vol_txt)
        
            if change > 15 and price < 40 and volume > 10000:
                stock_list[ticker] = (change, price, volume)

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
    # Cookie = '__eoi=ID=240fa7f019267950:T=1740316804:RT=1740316804:S=AA-AfjbJp4H6baKAFJLYgth0Fbct;__gads=ID=e3d5adff96d0e7b4:T=1740316804:RT=1740316804:S=ALNI_MaAmyI4r-yviDtc506P4aWLFEsjJQ;__gpi=UID=00001048cbf5bdd0:T=1740316804:RT=1740316804:S=ALNI_MbIr5Z5Kmw6Qw8G7MAjrp4MWyMcbA;_ga=GA1.1.1233108505.1738595349;_ga_YVVRYGL0E0=GS1.1.1741352370.39.1.1741353180.58.0.0;_sp_id.cf1a=417e44ab-7e61-4e3e-9886-7b243d437dfc.1731934501.21.1741353180.1741271899.8a8fc797-8bd2-46e0-a400-b2b30eefb8c9.f72d2d44-f6e9-4b91-847b-f81ed81dd724.bcbdc5c7-bf54-40c2-b019-cb6805560687.1741352892554.3;_sp_ses.cf1a=*;cachec=3f045c69-fd72-42a7-95d3-924c2cc6b302;cookiePrivacyPreferenceBannerProduction=accepted;cookiesSettings={"analytics":true,"advertising":true};device_t=VDYxeUJROjIsb2RGa0JROjMsREptZEJROjE.7jsVyj-98b8JeONequwC9Gw_BJDEXTEIedMB37MAWVk;etg=3f045c69-fd72-42a7-95d3-924c2cc6b302;png=3f045c69-fd72-42a7-95d3-924c2cc6b302;sessionid=6ldhwhjneb6nn2sl1a2lk01zglv55t34;sessionid_sign=v3:lEoqyYNitbAlvrJrzGd6cYHCXq6j5AJUkZzcrkQTtUw=;theme=light;tv_ecuid=3f045c69-fd72-42a7-95d3-924c2cc6b302;'
    Cookie = '__eoi=ID=240fa7f019267950:T=1740316804:RT=1747651979:S=AA-AfjbJp4H6baKAFJLYgth0Fbct;__gads=ID=e3d5adff96d0e7b4:T=1740316804:RT=1747651979:S=ALNI_MaAmyI4r-yviDtc506P4aWLFEsjJQ;__gpi=UID=00001048cbf5bdd0:T=1740316804:RT=1747651979:S=ALNI_MbIr5Z5Kmw6Qw8G7MAjrp4MWyMcbA;_ga=GA1.1.1233108505.1738595349;_ga_YVVRYGL0E0=GS2.1.s1747651911$o745$g1$t1747652254$j23$l0$h0;_sp_id.cf1a=417e44ab-7e61-4e3e-9886-7b243d437dfc.1731934501.70.1747652227.1747408035.38a10d4b-fa28-4298-afcd-3476e711da77.78bc881c-c40a-497f-975e-6efa34cbdd46.0b095410-1d0d-443d-b7db-61b50600e59b.1747651911757.19;_sp_ses.cf1a=*;cachec=3f045c69-fd72-42a7-95d3-924c2cc6b302;cookiePrivacyPreferenceBannerProduction=accepted;cookiesSettings={"analytics":true,"advertising":true};device_t=VDYxeUJROjIsdVlqb0JROjEsOHNnWEJnOjE.LyJmiZYrY3VZkUvJvxOYb57zP1S02T8VEy3bJhrlraQ;etg=3f045c69-fd72-42a7-95d3-924c2cc6b302;png=3f045c69-fd72-42a7-95d3-924c2cc6b302;sessionid=enrlyz3h3k1mumhlrboq344agemujuk5;sessionid_sign=v3:nI38imZcTGRyxkuqogw//LtBYE1jS+EjYk6Hp3avLFI=;theme=light;tv_ecuid=3f045c69-fd72-42a7-95d3-924c2cc6b302;'
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
        save_last_20_min_data(is_pre, list_rows, stock_list)

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

if __name__ == '__main__':
    get_request(True, {})