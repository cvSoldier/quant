import backtrader as bt
import pandas as pd

class KLineStrategy(bt.Strategy):
    params = (
        ('n', 20),      # 形态周期
        ('p', 5.0),     # 上涨幅度百分比
        ('stop_percent', 3.0),  # 止盈止损百分比
    )

    def __init__(self):
        # 初始化指标引用
        self.close = self.datas[0].close
        self.high = self.datas[0].high
        
        # 计算n周期前的收盘价
        self.close_n = bt.indicators.Highest(self.close(-self.params.n), period=self.params.n)
        
        # 计算n周期内最高价
        self.highest_high = bt.indicators.Highest(self.high, period=self.params.n)

    def next(self):
        # 避免在初始阶段计算
        if len(self) < self.params.n:
            return

        # 条件1: 最高价相比n周期前收盘价上涨p%
        cond_up = self.highest_high[0] >= self.close_n[0] * (1 + self.params.p / 100)
        
        # 条件2: 当前收盘价高于前一根收盘价
        cond_reversal = self.close[0] > self.close[-1]
        
        # 条件3: 当前收盘价低于最高价（处于下跌阶段）
        cond_downtrend = self.close[0] < self.highest_high[0]
        
        # 综合买入条件
        if cond_up and cond_reversal and cond_downtrend:
            # 计算头寸规模（全仓买入）
            size = self.broker.getcash() / self.close[0]
            # 发出买入订单
            self.order = self.buy(size=size)
            
            # 计算止盈止损价格
            entry_price = self.close[0]
            stop_loss = entry_price * (1 - self.params.stop_percent / 100)
            take_profit = entry_price * (1 + self.params.stop_percent / 100)
            
            # 添加止盈止损订单（bracket订单）
            self.sell(exectype=bt.Order.Limit, price=take_profit, parent=self.order)
            self.sell(exectype=bt.Order.Stop, price=stop_loss, parent=self.order)

    def notify_order(self, order):
        # 订单状态监控
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f'买入 @ {order.executed.price:.2f}')
            elif order.issell():
                print(f'卖出 @ {order.executed.price:.2f}')

# 初始化回测引擎
cerebro = bt.Cerebro()

# 加载数据（示例数据，需替换为实际数据）
data = bt.feeds.GenericCSVData(
    dataname='/Users/wyc/CODE/quant/xrp/data/XRPUSDT_5m_full.csv',
    dtformat=('%Y-%m-%d %H:%M:%S'),
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
    timeframe=bt.TimeFrame.Minutes,  # 时间周期为分钟
    compression=5,  # 5分钟
    openinterest=-1
)
cerebro.adddata(data)

# 添加策略
cerebro.addstrategy(KLineStrategy)

# 设置初始资金
cerebro.broker.setcash(100000.0)

# 运行回测
print('初始资金: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('最终资金: %.2f' % cerebro.broker.getvalue())

# 可视化（需安装matplotlib）
cerebro.plot()