import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QAbstractItemView, QVBoxLayout, QWidget, 
                             QPushButton, QLabel)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from price import do_scan
from news import get_news

# 工作线程类，用于后台执行数据扫描
class ScanThread(QThread):
    # 定义一个信号，用于传递扫描结果
    data_ready = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.last_scan_data = []
        self.running = True
        
    def run(self):
        while self.running:
            # 执行数据扫描
            res = []
            price_data_list = do_scan()
            last_code_list = [item['code'] for item in self.last_scan_data]
            
            for item in price_data_list:
                code_data = next((_item for _item in self.last_scan_data if item['code'] == _item['code']), None)
                is_new_news = code_data and code_data.get('date', None) and ('min' in code_data['date'] or 'hour' in code_data['date'])
                if not (item['code'] in last_code_list and is_new_news):
                    print(f'{item['code']} news')
                    news_data = get_news(item['code'])
                    if news_data:
                        item.update(news_data)
                res.append(item)
                
            self.last_scan_data = res
            # 发送扫描结果给主线程
            self.data_ready.emit(res)
            
            # 等待10秒，但不阻塞主线程
            for _ in range(100):
                if not self.running:
                    return
                time.sleep(0.1)  # 每次休眠0.1秒
    
    def stop(self):
        """停止线程"""
        self.running = False

class StockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("冷静交易")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主部件和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["股票代码", "涨幅", "新闻", "新闻时间", "操作"])
        
        # 设置表格属性
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        self.layout.addWidget(self.table)
        
        # 添加状态标签
        self.status_label = QLabel("上次更新时间: 从未更新")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)
        
        # 创建并启动工作线程
        self.scan_thread = ScanThread()
        self.scan_thread.data_ready.connect(self.update_table)
        self.scan_thread.start()
        
        # 设置定时器用于更新状态
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # 每秒更新一次状态
    
    def update_status(self):
        """更新状态标签，显示最后更新时间"""
        if hasattr(self, 'last_update_time'):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", self.last_update_time)
            self.status_label.setText(f"上次更新时间: {current_time}")
    
    def update_table(self, data):
        """在UI线程中安全地更新表格"""
        # 记录更新时间
        self.last_update_time = time.localtime()
        
        # 设置表格行数
        self.table.setRowCount(len(data))
        
        # 填充数据
        for row, stock in enumerate(data):
            # 股票代码
            self.table.setItem(row, 0, QTableWidgetItem(stock.get("code", '')))
            
            # 涨幅 - 根据正负设置不同颜色
            change_item = QTableWidgetItem(stock["change"])
            self.table.setItem(row, 1, change_item)
            
            # 新闻内容
            news_item = QTableWidgetItem(stock.get("title", ''))
            news_item.setToolTip(stock.get("title", ''))  # 添加悬停提示
            self.table.setItem(row, 2, news_item)
            self.table.setItem(row, 3, QTableWidgetItem(stock.get("date", '')))
            
            # 买入按钮
            btn_buy = QPushButton("买入")
            btn_buy.setProperty("stock_code", stock["code"])
            # btn_buy.setEnabled(stock["can_buy"])
            btn_buy.clicked.connect(lambda _, c=stock["code"]: self.buy_stock(c))
            self.table.setCellWidget(row, 4, btn_buy)
    
    def buy_stock(self, stock_code):
        """处理买入按钮点击事件"""
        print(f"买入股票: {stock_code}")
        # 这里应该执行实际的买入操作
        # 例如：调用API、显示确认对话框等
        self.status_label.setText(f"尝试买入股票: {stock_code} - 等待确认...")
        
        # 显示确认对话框的示例
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, '确认买入',
                                     f'确认买入 {stock_code} 吗?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 执行买入操作
            self.status_label.setText(f"已提交买入 {stock_code} 的订单")
    
    def closeEvent(self, event):
        """确保在窗口关闭时停止线程"""
        self.scan_thread.stop()
        self.scan_thread.wait()  # 等待线程结束
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockApp()
    window.show()
    sys.exit(app.exec_())