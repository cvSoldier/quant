# 不好用，代理了之后除了浏览器的请求，其他（比如抓news和翻译）都有问题

from mitmproxy import http, ctx
import json
from news import get_news

def configure(updated):
    """MANDATORY 配置函数"""
    if not updated:
        # 关闭所有常规日志，只显示错误
        ctx.options.console_verbosity = "error"
        
        # 禁止事件日志（连接/断开等）
        ctx.options.console_eventlog = False
        
        # 可选：禁用流日志（HTTP流量）
        # ctx.options.console_flowlist = False

def response(flow: http.HTTPFlow) -> None:
    """仅处理目标扫描请求的响应"""
    # 1. 精准识别目标请求
    target_host = "scanner.tradingview.com"
    target_path = "/america/scan"
    
    # 仅处理特定域名的扫描请求
    if flow.request.pretty_host == target_host and flow.request.path.startswith(target_path):
        # 使用打印而非ctx.log避免全局设置干扰
        print("\n" + "="*80)
        print(f"📡 拦截到 TradingView 扫描请求: {flow.request.url}")
        
        try:
            # 解析并输出JSON响应
            data = flow.response.json()
            
            # print(f"📋 响应片段:\n{json.dumps(data, indent=2)[:500]}...")
            # stock_data_list = data['data']
            # for stock_data in stock_data_list:
            #     stock_d = stock_data['d']
            #     name = stock_d[0]
            #     news = get_news(name)
            
            # 响应统计
            print(f"\n⏱️ 响应时间: {flow.response.timestamp_end - flow.response.timestamp_start:.3f}秒")
            print(f"📦 响应大小: {len(flow.response.content)}字节")
            print("="*80 + "\n")
            
        except json.JSONDecodeError:
            print("⚠️ JSON解析失败！原始响应:")
            print(flow.response.text[:500] + ("..." if len(flow.response.text) > 500 else ""))
        except Exception as e:
            print(f"🚨 处理错误: {str(e)}")