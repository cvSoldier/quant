import requests
from bs4 import BeautifulSoup
from translate import Translator
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler

trans_cache_dict = {}
news_cache_dict= {}
# 每10s访问一次，新闻过期时间为30s
CACHE_DISABLE_TIMES = 3

def time_ago(time_str, time_format='%m/%d/%Y %H:%M'):
    """
    计算给定时间距离现在多久以前，返回自然语言描述
    
    参数:
        time_str: 时间字符串，如 '06/06/2025 21:00'
        time_format: 时间字符串的格式，默认为 '%m/%d/%Y %H:%M'
    
    返回:
        相对时间描述字符串，如 '2 minutes ago', '3 days ago'
    """
    # 解析输入时间
    given_time = datetime.strptime(time_str, time_format)
    now = datetime.now()
    
    # 计算时间差
    delta = relativedelta(now, given_time)
    
    # 判断时间差并返回相应描述
    if delta.years > 0:
        return f"{delta.years} year{'s' if delta.years > 1 else ''} ago"
    elif delta.months > 0:
        return f"{delta.months} month{'s' if delta.months > 1 else ''} ago"
    elif delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.hours > 0:
        return f"{delta.hours} hour{'s' if delta.hours > 1 else ''} ago"
    elif delta.minutes > 0:
        return f"{delta.minutes} minute{'s' if delta.minutes > 1 else ''} ago"
    else:
        return "just now"


def convert_us_to_shanghai_time(time_str):
    # 定义时区
    eastern = pytz.timezone('America/New_York')  # 美国东部时间
    shanghai = pytz.timezone('Asia/Shanghai')    # 上海时间
    
    # 解析美国时间字符串（格式：月/日/年 时:分 AM/PM）
    try:
      us_time = datetime.strptime(time_str, '%m/%d/%Y\n%I:%M %p')
    except Exception as e:
        print(f"发生错误: {str(e)}")
    
    # 本地化到美国东部时区
    us_time = eastern.localize(us_time)
    
    # 转换为上海时间
    shanghai_time = us_time.astimezone(shanghai)
    
    # 格式化为24小时制字符串
    return shanghai_time.strftime('%m/%d/%Y %H:%M')



def ggtran(text,dest='zh-cn', src='auto'):
    translation = ''
    try:
        translator = Translator(to_lang="zh")
        translation = translator.translate(text)
    except Exception as e:
        print(f"翻译发生错误: {str(e)}")
    finally:
        return translation

def get_news(stock_code):
    is_new_stock = False
    if stock_code in news_cache_dict:
        news_cache = news_cache_dict[stock_code]
        if news_cache['visit_times'] < CACHE_DISABLE_TIMES:
            news_cache['visit_times'] = news_cache['visit_times'] + 1
            return news_cache['news']
    else:
        is_new_stock = True
        import os
        # 仅Mac系统
        os.system('afplay /Users/wyc/CODE/quant/scanner_v3/notify.mp3')

    url = f"https://www.stocktitan.net/news/{stock_code}/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    news_data = None
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()  # 检查HTTP错误
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='news-feed-content')
        
        lastest_news = news_items[0]
        title_ori = lastest_news.find('h2').text.strip()
        date = lastest_news.find('time').text.strip()
        
        date = convert_us_to_shanghai_time(date)
        date = time_ago(date)
        if title_ori in trans_cache_dict:
            title = trans_cache_dict[title_ori]
        else:
            title = ggtran(title_ori)
            trans_cache_dict[title_ori] = title
        if title == '':
            title = title_ori
        news_data = {
            'name': stock_code,
            'title_ori': title_ori,
            'title': title,
            'date': date,
            'is_new_stock': is_new_stock
        }
        news_cache_dict[stock_code] = {
            'visit_times': 0,
            'news': news_data
        }
        return news_data

    except requests.exceptions.RequestException as e:
        print("请求错误:", e)
    finally:
        return news_data

def job():
    print(get_news('prph'))

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")  # 设置时区（根据需求修改）

    # 添加每分钟触发一次的调度任务
    scheduler.add_job(job, 'interval', seconds=10)

    try:
        print("调度器启动，按 Ctrl+C 退出...")
        job()
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("调度器已关闭")