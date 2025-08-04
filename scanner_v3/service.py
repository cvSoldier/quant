from flask import Flask, request, jsonify
import json
from news import get_news

# # 假设这是您已经存在的 get_news 方法
# def get_news(stock_name):
#     """模拟获取股票新闻的函数，实际使用时替换为您的实现"""
#     # 这里只是一个示例实现
#     return [
#         {
#             "stock": stock_name,
#             "title": f"{stock_name}宣布突破性技术创新",
#             "source": "金融时报",
#             "date": "2023-06-15"
#         },
#         {
#             "stock": stock_name,
#             "title": f"分析师看好{stock_name}的长期增长前景",
#             "source": "华尔街日报",
#             "date": "2023-06-14"
#         }
#     ]

app = Flask(__name__)

@app.route('/get_news', methods=['GET'])
def news_endpoint():
    # 从查询参数获取股票名称
    stock_name = request.args.get('stock_name')
    
    if not stock_name:
        return jsonify({"error": "缺少 stock_name 参数"}), 400
    
    # 调用现有的 get_news 函数
    news_data = get_news(stock_name.split(':')[1])
    
    # 将结果转换为 JSON 格式返回
    return jsonify(news_data)

if __name__ == '__main__':
    # 启动服务，监听所有 IP，端口 5000
    app.run(host='0.0.0.0', port=5001)