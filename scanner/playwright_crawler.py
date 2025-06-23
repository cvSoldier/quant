import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

# 全局浏览器实例和 Playwright 对象
browser = None
pw = None

def time_ago(time_str, time_format='%m/%d/%Y %H:%M'):
    """计算相对时间"""
    given_time = datetime.strptime(time_str, time_format)
    now = datetime.now()
    delta = relativedelta(now, given_time)
    
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
    """转换美国时间到上海时间"""
    eastern = pytz.timezone('America/New_York')
    shanghai = pytz.timezone('Asia/Shanghai')
    us_time = datetime.strptime(time_str, '%m/%d/%Y %I:%M %p')
    us_time = eastern.localize(us_time)
    shanghai_time = us_time.astimezone(shanghai)
    return shanghai_time.strftime('%m/%d/%Y %H:%M')

async def init_browser():
    """初始化并返回 Playwright 浏览器实例"""
    global browser, pw
    
    if browser is None or not browser.is_connected():
        if pw is None:
            pw = await async_playwright().start()
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--window-size=1920,1080",
                "--disable-dev-shm-usage"
            ]
        )
    return browser

async def close_browser():
    """关闭浏览器实例（程序结束时调用）"""
    global browser, pw
    if browser:
        await browser.close()
        browser = None
    if pw:
        await pw.stop()
        pw = None

async def get_news_by_stocktitan(context, stock_code):
    """使用 Playwright 从 StockTitan 获取新闻"""
    try:
        news_data = {}
        page = await context.new_page()
        url = f'https://www.stocktitan.net/news/{stock_code}/'
        await page.goto(url, timeout=15000)
        
        # 等待元素加载并获取数据
        await page.wait_for_selector(".company-list", timeout=10000)
        stream_content = await page.query_selector(".news-feed-content")
        
        if stream_content:
            title_elem = await stream_content.query_selector("h2")
            news_data["title"] = await title_elem.inner_text() if title_elem else ""
            
            time_elem = await stream_content.query_selector("time")
            news_data["time"] = await time_elem.inner_text() if time_elem else ""
            
            # 检查是否有效获取数据
            if news_data.get("title") and news_data.get("time"):
                return news_data
        return None
    except Exception as e:
        print(f"StockTitan 获取 {stock_code} 新闻时出错: {str(e)}")
        return None
    finally:
        await page.close()

async def get_news_by_yahoo(context, stock_code):
    """使用 Playwright 从 Yahoo Finance 获取新闻"""
    try:
        news_data = {}
        page = await context.new_page()
        url = f"https://finance.yahoo.com/quote/{stock_code}/news/"
        await page.goto(url, timeout=60000)
        
        # 等待元素加载
        await page.wait_for_selector("ul.stream-items", timeout=10000)
        
        # 获取第一条新闻内容
        stream_content = await page.query_selector("ul.stream-items li:first-child .content")
        
        if stream_content:
            # 提取标题
            title_elem = await stream_content.query_selector("h3")
            news_data["title"] = await title_elem.inner_text() if title_elem else ""
            
            # 提取时间信息
            source_elem = await stream_content.query_selector(".publishing")
            if source_elem:
                source_text = await source_elem.inner_text()
                source_text = source_text.replace('\n', '').replace('\r', '')
                
                # 解析时间格式
                if '•' in source_text:
                    _, _, time_part = source_text.partition('•')
                    news_data["time"] = time_part.strip()
                else:
                    news_data["time"] = source_text.strip()
            
            # 检查是否有效获取数据
            if news_data.get("title") and news_data.get("time"):
                return news_data
        return None
    except Exception as e:
        print(f"Yahoo 获取 {stock_code} 新闻时出错: {str(e)}")
        return None
    finally:
        await page.close()

async def _get_news_data(stock_code):
    """异步获取股票新闻数据（主函数）"""
    try:
        # 获取或创建浏览器实例
        browser = await init_browser()
        
        # 创建独立的浏览器上下文
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        # 尝试不同来源获取新闻
        news_data = None
        news_data = await get_news_by_stocktitan(context, stock_code)
        if not news_data:
            news_data = await get_news_by_yahoo(context, stock_code)
        else:
            try:
                news_data['time'] = convert_us_to_shanghai_time(news_data['time'])
                news_data['time'] = time_ago(news_data['time'])
            except Exception as e:
                print(f"时间处理错误: {str(e)}")
        
        return news_data
    except Exception as e:
        print(f"股票 {stock_code} 获取新闻时发生错误: {str(e)}")
        return None
    finally:
        # 关闭上下文（不关闭浏览器）
        if 'context' in locals() and context:
            await context.close()

async def get_news_data_async(stock_codes):
    """主异步函数，处理多个股票代码"""
    results = {}
    
    # 使用信号量控制并发度（避免过多并发导致资源耗尽）
    sem = asyncio.Semaphore(2)  # 最多同时5个请求
    
    async def fetch_stock(stock_code):
        async with sem:
            return stock_code, await _get_news_data(stock_code)
    
    # 创建并执行所有任务
    tasks = [fetch_stock(code) for code in stock_codes]
    stock_results = await asyncio.gather(*tasks)
    
    # 整理结果
    for stock_code, news in stock_results:
        results[stock_code] = news
    
    # 程序结束时关闭浏览器
    await close_browser()
    return results

if __name__ == "__main__":
    # 示例股票代码列表
    # todo
    # 大票的新闻很杂 不确定 测试用小票
    # stocks = ['KNW']
    stocks = ['KNW', 'PRZO', 'MSFT', 'AIHS', 'FAAS', 'PLRZ']
    
    # 运行异步主程序
    results = asyncio.run(get_news_data_async(stocks))
    
    # 输出结果
    for stock, news in results.items():
        print(f"\n=== {stock} ===")
        if news:
            print(f"标题: {news.get('title', '无')}")
            print(f"时间: {news.get('time', '无')}")
        else:
            print("未获取到新闻数据")
    # close_browser()