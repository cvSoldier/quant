from flask import Flask, request, jsonify
import json
from news import get_news

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