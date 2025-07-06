from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

from selenium.webdriver.chrome.service import Service

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式（取消注释可在有界面模式下调试）
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# 自定义等待条件：等待任意一个元素出现
class AnyElementLocated:
    def __init__(self, locators):
        self.locators = locators
    
    def __call__(self, driver):
        for locator in self.locators:
            elements = driver.find_elements(*locator)
            if elements and elements[0].is_displayed():
                return elements[0]
        return False


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
    us_time = datetime.strptime(time_str, '%m/%d/%Y %I:%M %p')
    
    # 本地化到美国东部时区
    us_time = eastern.localize(us_time)
    
    # 转换为上海时间
    shanghai_time = us_time.astimezone(shanghai)
    
    # 格式化为24小时制字符串
    return shanghai_time.strftime('%m/%d/%Y %H:%M')


def init_selenium():
    pass

def get_news_by_stocktitan(driver, stock_code):
    try:
        news_data = {}
        url = f'https://www.stocktitan.net/news/{stock_code}/'
        driver.get(url)
        # 显式等待页面加载 - 使用更稳健的选择器
        wait = WebDriverWait(driver, 15)
        company_list = wait.until(
            AnyElementLocated([
                (By.CSS_SELECTOR, ".company-list"),
                (By.CSS_SELECTOR, ".error-code")
            ])
        )
        element_class = company_list.get_attribute("class")
        if "error-code" in element_class:
            news_data = None
            return news_data
        stream_content = company_list.find_element(By.CSS_SELECTOR, ".news-feed-content")
        title_elem = stream_content.find_element(By.CSS_SELECTOR, "h2")
        news_data["title"] = title_elem.text
        time_elem = stream_content.find_element(By.CSS_SELECTOR, "time")
        news_data["time"] = time_elem.text
    except Exception as e:
        print(f"发生错误: {str(e)}")
        news_data = None
    finally:
        return news_data

def get_news_by_yahoo(driver, stock_code):
    news_data = {}
    url = f"https://finance.yahoo.com/quote/{stock_code}/news/"
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    
    # 等待ul.stream-items出现
    stream_content = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "ul.stream-items li:first-child .content"
        ))
    )
    
    # 1. 标题
    title_elem = stream_content.find_element(By.CSS_SELECTOR, "h3")
    news_data["title"] = title_elem.text
    source_elem = stream_content.find_element(By.CSS_SELECTOR, ".publishing")
    before, sep, after = source_elem.text.replace('\n', '').replace('\r', '').partition('•')
    if sep:  # 如果找到分隔符
        news_data["time"] = after
    else:
        news_data["time"] = source_elem.text
    
    return news_data


def get_news_data(stock_code):
    # 设置Chrome驱动
    # service = Service(executable_path="chromedriver.exe")  # 根据实际情况修改路径
    driver = webdriver.Chrome(options=chrome_options)
    try:
        news_data = None
        news_data = get_news_by_stocktitan(driver, stock_code)
        if news_data is None:
            news_data = get_news_by_yahoo(driver, stock_code)
        else:
            news_data['time'] = convert_us_to_shanghai_time(news_data['time'])
            news_data['time'] = time_ago(news_data['time'])
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        # 关闭浏览器
        driver.quit()
        return news_data

if __name__ == "__main__":
    result = get_news_data('MINM')
    if result:
        print(result)
    else:
        print("\n未能抓取数据，请检查错误信息")