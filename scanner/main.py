from datetime import datetime, time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from use_request import get_request
import redirect_print

CURENT_IDX = 0
TOTAL_LEN = 20
arr_2d = [{} for _ in range(TOTAL_LEN)]


def target(is_pre):
    """需要定时执行的目标函数"""
    global CURENT_IDX
    
    already_in_stock_name = {}
    for d in arr_2d:
        already_in_stock_name.update(d)

    get_request(is_pre, arr_2d[CURENT_IDX])

    result = []
    for key, val in arr_2d[CURENT_IDX].items():
        if key not in already_in_stock_name:
            result.append(key)
        else:
            order_arr_2d = reorder_array(arr_2d, CURENT_IDX)
            # TODO

    # 获取当前时间
    now = datetime.now()
    print(now)
    # print(result)
    for stock_name in result:
        print(stock_name)
        print('https://cn.tradingview.com/chart/Iauyrdyx/?symbol=NASDAQ%3A' + stock_name)
        print(f'https://finance.yahoo.com/quote/{stock_name}/')

    CURENT_IDX += 1
    CURENT_IDX = CURENT_IDX % TOTAL_LEN

def reorder_array(arr, index):
    n = len(arr)
    start = (index + 1) % n  # 计算起始位置并确保不越界
    return [arr[(start + i) % n] for i in range(n)]


def is_time_in_range(start_time, end_time):
    """检查当前时间是否在指定时间范围内"""
    now = datetime.now().time()
    if start_time <= end_time:
        return start_time <= now <= end_time
    else:
        return now >= start_time or now <= end_time

def job():
    """调度任务：仅在时间范围内执行 target"""
    start = time(16, 0)    # 开始时间 16:00
    middle = time(21, 30)     # 结束时间 21:30
    end = time(23, 30)
    if is_time_in_range(start, middle):
        target(True)
    elif is_time_in_range(middle, end):
        target(False)

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")  # 设置时区（根据需求修改）

    # 添加每分钟触发一次的调度任务
    scheduler.add_job(job, 'interval', minutes=1)

    try:
        print("调度器启动，按 Ctrl+C 退出...")
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("调度器已关闭")