// ==UserScript==
// @name         tradingview
// @namespace    https://bbs.tampermonkey.net.cn/
// @version      0.1.0
// @description  try to take over the world!
// @author       You
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// @connect      localhost
// @connect      papertrading.tradingview.com
// @match        https://cn.tradingview.com/chart/DpA5nKu2/?source=promo_go_pro_button
// @require      https://scriptcat.org/lib/637/1.4.7/ajaxHooker.js
// ==/UserScript==

async function fetchStockNews(stockName) {
  return new Promise((resolve, reject) => {
      GM_xmlhttpRequest({
          method: "GET",
          url: `http://localhost:5001/get_news?stock_name=${encodeURIComponent(stockName)}`,
          onload: function(response) {
              try {
                  const data = JSON.parse(response.responseText);
                  resolve(data);
              } catch (e) {
                  reject(new Error('Failed to parse JSON'));
              }
          },
          onerror: reject,
          timeout: 5000
      });
  });
}
function vision_btn(btn) {
   // 添加视觉反馈
   btn.style.transform = 'scale(0.9)';
   btn.style.backgroundColor = '#ffeb3b';
   setTimeout(() => {
       btn.style.transform = '';
       btn.style.backgroundColor = '';
   }, 300);
}

(function() {
   'use strict';

   var INVALID_PRICE = 100
   var fund_remain = 0
   var cur_price = INVALID_PRICE
   var cur_stock_symbol = ''
   var stock_num = 0
   var account_id = 0

   function setInputValueWithEvents(input, value) {
   // 1. 聚焦到元素
       input.focus();
       
       // 2. 更新实际值
       input.value = value;
       
       // 3. 触发各种事件模拟真实输入
       const events = [
           'keydown', 'keypress', 'input', 'keyup', 'change', 'blur'
       ];
       
       events.forEach(eventType => {
           const event = new Event(eventType, { 
               bubbles: true,
               cancelable: true
           });
           
           // 对于input事件，添加额外的数据特性
           if (eventType === 'input') {
               Object.defineProperty(event, 'target', {
                   value: { value: input.value },
                   writable: false
               });
           }
           
           input.dispatchEvent(event);
       });
       
       // 4. 特殊处理 React 可能需要的合成事件
       try {
           const reactEvent = new Event('change', { bubbles: true });
           Object.defineProperty(reactEvent, 'target', { 
               value: { value: input.value }, 
               writable: false 
           });
           input.dispatchEvent(reactEvent);
       } catch (e) {
           console.log("React 特殊事件处理失败", e);
       }
   }

   function handleClick(event) {
       var tr_ele = event.target.closest('tr');
       if (tr_ele && tr_ele.dataset.rowkey) {
           cur_stock_symbol = tr_ele.dataset.rowkey;
       }
   }
   function get_stock_symbol() {
       document.querySelectorAll('.listRow').forEach(element => {
           element.addEventListener('click', handleClick);
       });
   }
   function buy_in() {
       var qty = Math.floor(fund_remain * 0.95 / cur_price)
       const tradeData = {
           symbol: cur_stock_symbol,
           type: "limit",
           qty: qty,
           side: "buy",
           price: cur_price,
           outside_rth: true,
           outside_rth_tp: false,
           expiration: 1754834810
       };
       console.log(tradeData)

       var buy_side = document.getElementsByClassName('buy-B5GOsH7j')[0]
       buy_side.click()
       document.querySelector("#absolute-limit-price-field").value = cur_price;

       var qty_dom = document.querySelector("#quantity-field")
       // qty_dom.value = String(qty);
       setInputValueWithEvents(qty_dom, qty)
       
       // var done_btn = document.getElementsByClassName('button-pP_E6i3F')[0]
       // done_btn.click()
   }

   // 添加按钮组样式
   GM_addStyle(`
       #draggable-btn-group {
           position: fixed;
           top: 100px;
           left: 20px;
           z-index: 9999;
           background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
           border-radius: 12px;
           padding: 15px;
           box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
           display: flex;
           gap: 12px;
           cursor: move;
           border: 2px solid rgba(255, 255, 255, 0.2);
           backdrop-filter: blur(10px);
           transition: transform 0.2s, box-shadow 0.2s;
       }
       
       #draggable-btn-group:hover {
           transform: translateY(-2px);
           box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
       }
       
       .draggable-btn {
           width: 50px;
           height: 50px;
           border-radius: 50%;
           background: rgba(255, 255, 255, 0.9);
           color: #2575fc;
           font-weight: bold;
           font-size: 18px;
           border: none;
           cursor: pointer;
           box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
           transition: all 0.3s ease;
           display: flex;
           justify-content: center;
           align-items: center;
       }
       
       .draggable-btn:hover {
           background: white;
           transform: scale(1.1);
           box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
       }
       
       .draggable-btn:active {
           transform: scale(0.95);
       }
       
       .btn-1 { color: #e74c3c; }
       .btn-2 { color: #27ae60; }
       .btn-3 { color: #f39c12; }
       
       .handle {
           position: absolute;
           top: -15px;
           left: 0;
           right: 0;
           height: 15px;
           cursor: move;
       }
   `);

   // 创建按钮组
   const btnGroup = document.createElement('div');
   btnGroup.id = 'draggable-btn-group';
   btnGroup.innerHTML = `
       <div class="handle"></div>
       <button class="draggable-btn btn-1">入</button>
       <button class="draggable-btn btn-2">半出</button>
       <button class="draggable-btn btn-3">全出</button>
   `;
   
   // 添加按钮组到页面
   setTimeout(() => {
       document.body.appendChild(btnGroup);
   }, 2000)

   // 添加按钮点击事件
   const buttons = btnGroup.querySelectorAll('.draggable-btn');
   buttons.forEach((btn, index) => {
       if(index === 0) {
           btn.addEventListener('click', () => {
               buy_in()
               vision_btn(btn)
           });
       } else if (index === 1) {
           btn.addEventListener('click', () => {
               sell_half()
               vision_btn(btn)
           });
       } else if (index === 2) {
           btn.addEventListener('click', () => {
               sell_all()
               vision_btn(btn)
           });
       }
   });

   // 实现拖动功能
   let isDragging = false;
   let offsetX, offsetY;
   
   const handle = btnGroup.querySelector('.handle');
   const bar = btnGroup;
   
   const startDrag = (e) => {
       if (e.target === btnGroup || e.target === handle) {
           isDragging = true;
           const rect = btnGroup.getBoundingClientRect();
           offsetX = e.clientX - rect.left;
           offsetY = e.clientY - rect.top;
           btnGroup.style.cursor = 'grabbing';
           btnGroup.style.opacity = '0.9';
           e.preventDefault();
       }
   };
   
   const onDrag = (e) => {
       if (!isDragging) return;
       btnGroup.style.left = (e.clientX - offsetX) + 'px';
       btnGroup.style.top = (e.clientY - offsetY) + 'px';
   };
   
   const stopDrag = () => {
       isDragging = false;
       btnGroup.style.cursor = 'move';
       btnGroup.style.opacity = '';
   };
   
   btnGroup.addEventListener('mousedown', startDrag);
   document.addEventListener('mousemove', onDrag);
   document.addEventListener('mouseup', stopDrag);


   var get_news_by_stock = (code) => {
       fetchStockNews(code).then(res => {
           const parentElement = document.querySelector('[data-rowkey="' + code + '"]');

           const news_datas = parentElement.getElementsByClassName('news_data');
           if(news_datas.length == 0) {
               const dateCell = document.createElement('td');
               dateCell.className = 'cell-RLhfr_y4 news_data';
               dateCell.textContent = res.date;
               parentElement.appendChild(dateCell);

               const newsCell = document.createElement('td');
               newsCell.className = 'cell-RLhfr_y4 news_data';
               newsCell.textContent = res.title;
               parentElement.appendChild(newsCell);
           } else {
               if(res) {
                   news_datas[0].innerText = res.date;
                   news_datas[1].innerText = res.title;
               }
           }
       })
       // 发送请求，然后渲染到这一行上
   }
   ajaxHooker.hook(request => {
       // 获取新闻到界面上
       if (request.url === 'https://scanner.tradingview.com/america/scan?label-product=popup-screener-stock') {
           request.response = res => {
               var data = res.json.data
               var stock_keys = data.map(item => item.s)
               stock_keys.map(get_news_by_stock)
               get_stock_symbol()
           };
       }
       // 获取账号剩余资金
       // TODO 交易之后也要更新余额
       if (request.url.includes('/trading/account/')) {
           request.response = res => {
               fund_remain = res.json.balance
               account_id = res.json.accountId
           };
       }
   });
   function splitMessageFrames(data) {
       const frames = [];
       let remaining = data;
       
       while (remaining.length > 0) {
           // 匹配帧头 ~m~{length}~m~
           const headerMatch = remaining.match(/^~m~(\d+)~m~/);
           if (!headerMatch) break;
           
           const headerLength = headerMatch[0].length;
           const contentLength = parseInt(headerMatch[1]);
           
           // 提取内容
           const content = remaining.substring(headerLength, headerLength + contentLength);
           frames.push(content);
           
           // 更新剩余内容
           remaining = remaining.substring(headerLength + contentLength);
       }
       
       return frames;
   }
   function parseMessageFrame(frame) {
       try {
           const data = JSON.parse(frame);
           
           // 只处理qsd消息
           if (data.m !== 'qsd') return null;
           
           // 提取价格信息
           const payload = data.p[1];
           if (!payload || !payload.v) return null;
           
           // 解析股票代码
           let stock_symbol = 'Unknown';
           if (payload.n) {
               if (payload.n.startsWith('={')) {
                   // 处理带参数的符号格式
                   const symbolData = JSON.parse(payload.n.slice(1));
                   stock_symbol = symbolData.stock_symbol || 'Unknown';
               } else {
                   stock_symbol = payload.n;
               }
           }
           
           // 提取价格
           // console.log(payload)
           const price = payload.v.ask || payload.v.rtc || payload.v.lp || INVALID_PRICE;
           return {
               stock_symbol,
               price,
           };
       } catch (e) {
           throw new Error('解析JSON失败: ' + e.message);
       }
   }

   // 保存原始WebSocket
   const NativeWebSocket = unsafeWindow.WebSocket;
   
   // 覆盖WebSocket构造函数
   unsafeWindow.WebSocket = function(url, protocols) {
       const targetPattern = /wss:\/\/prodata\.tradingview\.com\/socket\.io\/websocket/;
       if (typeof url === 'string' && targetPattern.test(url)) {
           console.log(`[WebSocket拦截器] 拦截到目标连接: ${url}`);
           
           const ws = new NativeWebSocket(url, protocols);
           
           // 增强拦截：监听所有消息事件
           const messageHandler = function(event) {
               try {
                   const data = event.data;
                   // console.log('[WebSocket拦截器] 收到消息:', data);
                   const messageFrames = splitMessageFrames(data);
           
                   // 解析每条消息
                   messageFrames.forEach(frame => {
                       try {
                           const parsed = parseMessageFrame(frame);
                           if (parsed) {
                               if (parsed.price != INVALID_PRICE) {
                                   cur_price = parsed.price
                               }
                           }
                       } catch (e) {
                           console.log(`解析错误: ${e.message}`);
                       }
                   });
               } catch (e) {
                   console.error('[WebSocket拦截器] 消息处理错误:', e);
               }
           };
           
           ws.addEventListener('message', messageHandler);
           
           // 添加关闭和错误监听
           ws.addEventListener('close', () => {
               console.log('[WebSocket拦截器] 连接关闭');
               ws.removeEventListener('message', messageHandler);
           });
           
           ws.addEventListener('error', (error) => {
               console.error('[WebSocket拦截器] 连接错误:', error);
           });
           
           return ws;
       }
       
       // 非目标连接使用原始WebSocket
       return new NativeWebSocket(url, protocols);
   };
   
   // 保留WebSocket原型
   unsafeWindow.WebSocket.prototype = NativeWebSocket.prototype;
})();