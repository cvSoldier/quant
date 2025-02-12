import backtrader as bt
import pandas as pd

import backtrader as bt

class KLineStrategy(bt.Strategy):
    params = (
        ('n', 20),      # 形态周期
        ('p', 5.0),     # 上涨幅度百分比
        ('stop_percent', 3.0),  # 止盈止损百分比
    )

    def __init__(self):
        self.close = self.datas[0].close
        self.high = self.datas[0].high
        
        # 关键修正：直接通过索引获取n周期前的收盘价序列
        self.close_n = self.close(-self.params.n)  # 延迟操作符
        
        # 计算n周期内最高价
        self.highest_high = bt.indicators.Highest(self.high, period=self.params.n)

    def next(self):
        if len(self) < self.params.n:
            return

        # 条件验证
        # TODO 不要20根，要不断向前找，找到确定的最低点，来看当前这波的涨幅的宽高
        cond_up = self.highest_high[0] >= self.close_n[0] * (1 + self.params.p / 100)
        # TODO 确定下跌的宽度，比如当前k线到最高点下跌k线的百分比 达到多少
        # TODO micro pullback的反转点是否可以通过成交量来体现？
        # TODO 卖出点 止盈 回到最高点出50%，剩下的逐渐出完，止损 在开单前一根的最低价
        cond_reversal = self.close[0] > self.close[-1]
        cond_downtrend = self.close[0] < self.highest_high[0]

        if cond_up and cond_reversal and cond_downtrend:
            # 计算头寸规模
            cash = self.broker.getcash()
            price = self.close[0]
            
            # 确保 price 有效且 cash 足够
            if price > 0 and cash > 0:
                size = cash / price
                if size > 0:  # 确保 size 有效
                    # 使用 buy_bracket 创建订单
                    self.order = self.buy_bracket(
                        size=size,
                        stopprice=price * (1 - self.params.stop_percent / 100),
                        limitprice=price * (1 + self.params.stop_percent / 100)
                    )
                    if self.order is None:
                        print("警告：buy_bracket 返回 None，订单未创建")
                else:
                    print(f"警告：size={size} 无效，无法创建订单")
            else:
                print(f"警告：cash={cash} 或 price={price} 无效，无法创建订单")
    def notify_order(self, order):
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
    timeframe=bt.TimeFrame.Minutes,  # 时间周期为分钟
    compression=5,  # 5分钟
    openinterest=-1
)
cerebro.adddata(data)

# 添加策略
cerebro.addstrategy(KLineStrategy)

# 设置初始资金
cerebro.broker.setcash(1000.0)

# 运行回测
print('初始资金: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('最终资金: %.2f' % cerebro.broker.getvalue())

# 可视化（需安装matplotlib）
cerebro.plot()