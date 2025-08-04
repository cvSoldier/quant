// ==UserScript==
// @name         tradingview
// @namespace    https://bbs.tampermonkey.net.cn/
// @version      0.1.0
// @description  try to take over the world!
// @author       You
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// @connect      localhost
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

   var fund_remain = 0
   var cur_price = 1
   var cur_stock_symbol = ''
   var stock_num = 0
   var account_id = 0

   function get_stock_symbol() {
       
   }
   function buy_in() {
       const tradeData = {
           symbol: "NASDAQ:LOBO",
           type: "limit",
           qty: 418.03,
           side: "buy",
           price: 0.7864,
           outside_rth: true,
           outside_rth_tp: false,
           expiration: 1754834810
       };

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
          timeout: 5000
      });
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
   document.body.appendChild(btnGroup);

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
               news_datas[0].innerText = res.date;
               news_datas[1].innerText = res.title;
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
   // Your code here...
})();