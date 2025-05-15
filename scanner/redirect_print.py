import sys
import datetime
import time

class DateFileLogger:
    def __init__(self):
        self.console = sys.stdout  # 保留原始控制台输出
        self.current_date = datetime.date.today()
        self.log_file = None
        self.open_log_file()  # 初始化日志文件

    def open_log_file(self):
        """根据当前日期打开或创建日志文件（追加模式）"""
        log_filename = self.current_date.strftime("%Y-%m-%d") + ".log"
        try:
            self.log_file = open(f'./log/{log_filename}', 'a', encoding='utf-8')
        except Exception as e:
            sys.stderr.write(f"无法打开日志文件: {e}\n")
            self.log_file = None

    def write(self, message):
        """重写 write 方法：输出到控制台和日志文件"""
        # 检查日期是否变化
        today = datetime.date.today()
        if today != self.current_date:
            if self.log_file:
                self.log_file.close()
            self.current_date = today
            self.open_log_file()
        # 写入控制台
        self.console.write(message)
        # 写入日志文件（如果可用）
        if self.log_file:
            self.log_file.write(message)
            self.log_file.flush()  # 确保立即写入磁盘

    def flush(self):
        """重写 flush 方法：同步刷新缓冲区"""
        self.console.flush()
        if self.log_file:
            self.log_file.flush()

# 重定向 sys.stdout
sys.stdout = DateFileLogger()

if __name__ == '__main__':
    while True:
        print(f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(2)  # 暂停 60 秒