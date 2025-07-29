fetch("https://papertrading.tradingview.com/trading/place/21392975", {
  "headers": {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,tk;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "cookie": "_ga=GA1.1.1233108505.1738595349; cookiesSettings={\"analytics\":true,\"advertising\":true}; cookiePrivacyPreferenceBannerProduction=accepted; theme=light; __gads=ID=e3d5adff96d0e7b4:T=1740316804:RT=1753061225:S=ALNI_MaAmyI4r-yviDtc506P4aWLFEsjJQ; __gpi=UID=00001048cbf5bdd0:T=1740316804:RT=1753061225:S=ALNI_MbIr5Z5Kmw6Qw8G7MAjrp4MWyMcbA; __eoi=ID=240fa7f019267950:T=1740316804:RT=1753061225:S=AA-AfjbJp4H6baKAFJLYgth0Fbct; device_t=VDYxeUJROjIsdVlqb0JROjEsOHNnWEJnOjEsWFpBWEJnOjIsRHROUkJnOjA.JoBF2Y1XC3b_-lZzEKKN7y8EFeboTIcqTffe85Q9tog; sessionid=csoqv9cplhmu4txhz0fzfxvkzc5ayfj3; sessionid_sign=v3:MIl9yy9hBAfhilIzrcG0gyzUpD+YVGfj+5SMnLsHqUI=; png=3f045c69-fd72-42a7-95d3-924c2cc6b302; etg=3f045c69-fd72-42a7-95d3-924c2cc6b302; cachec=3f045c69-fd72-42a7-95d3-924c2cc6b302; tv_ecuid=3f045c69-fd72-42a7-95d3-924c2cc6b302; _sp_ses.cf1a=*; _ga_YVVRYGL0E0=GS2.1.s1753534016$o1287$g1$t1753534129$j8$l0$h0; _sp_id.cf1a=417e44ab-7e61-4e3e-9886-7b243d437dfc.1731934501.146.1753534161.1753518362.4ac1e46d-c504-4de2-b179-99b675f838d5.87e9eadc-9cae-4443-8675-71e9108626bf.dbc99976-b066-498b-b500-6623aaeed596.1753534055366.3",
    "Referer": "https://cn.tradingview.com/"
  },
  "body": "{\"symbol\":\"NASDAQ:LHAI\",\"type\":\"limit\",\"qty\":9214.35,\"side\":\"buy\",\"price\":10.31,\"outside_rth\":true,\"outside_rth_tp\":false,\"expiration\":1753620560}",
  "method": "POST"
});
// 买入卖出通过payload中 side字段 区分
// {"symbol":"NASDAQ:LHAI","type":"limit","qty":9214.35,"side":"buy","price":10.31,"outside_rth":true,"outside_rth_tp":false,"expiration":1753620560}
// {"symbol":"NASDAQ:LHAI","type":"limit","qty":4849.66,"side":"sell","price":10.31,"outside_rth":true,"outside_rth_tp":false,"expiration":1753620927}
// 买入卖出请求为/place/账户id，取消为cancel/账户id， payload为{"id":2169406222},其中id为买入卖出response返回的id

// 当前使用账户的tradingview 信息
fetch("https://papertrading.tradingview.com/trading/account/21253291", {
  "headers": {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,tk;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "cookie": "_ga=GA1.1.1233108505.1738595349; cookiesSettings={\"analytics\":true,\"advertising\":true}; cookiePrivacyPreferenceBannerProduction=accepted; theme=light; __gads=ID=e3d5adff96d0e7b4:T=1740316804:RT=1753061225:S=ALNI_MaAmyI4r-yviDtc506P4aWLFEsjJQ; __gpi=UID=00001048cbf5bdd0:T=1740316804:RT=1753061225:S=ALNI_MbIr5Z5Kmw6Qw8G7MAjrp4MWyMcbA; __eoi=ID=240fa7f019267950:T=1740316804:RT=1753061225:S=AA-AfjbJp4H6baKAFJLYgth0Fbct; device_t=VDYxeUJROjIsdVlqb0JROjEsOHNnWEJnOjEsWFpBWEJnOjIsRHROUkJnOjA.JoBF2Y1XC3b_-lZzEKKN7y8EFeboTIcqTffe85Q9tog; sessionid=csoqv9cplhmu4txhz0fzfxvkzc5ayfj3; sessionid_sign=v3:MIl9yy9hBAfhilIzrcG0gyzUpD+YVGfj+5SMnLsHqUI=; png=3f045c69-fd72-42a7-95d3-924c2cc6b302; etg=3f045c69-fd72-42a7-95d3-924c2cc6b302; cachec=3f045c69-fd72-42a7-95d3-924c2cc6b302; tv_ecuid=3f045c69-fd72-42a7-95d3-924c2cc6b302; _sp_ses.cf1a=*; _ga_YVVRYGL0E0=GS2.1.s1753534016$o1287$g1$t1753534866$j60$l0$h0; _sp_id.cf1a=417e44ab-7e61-4e3e-9886-7b243d437dfc.1731934501.146.1753534866.1753518362.4ac1e46d-c504-4de2-b179-99b675f838d5.87e9eadc-9cae-4443-8675-71e9108626bf.dbc99976-b066-498b-b500-6623aaeed596.1753534055366.19",
    "Referer": "https://cn.tradingview.com/"
  },
  "body": "{}",
  "method": "POST"
});
// reponse中的balance字段为剩余资金

// 包含价格的链接
// wss://prodata.tradingview.com/socket.io/websocket?from=chart%2FDpA5nKu2%2F&date=2025-07-29T09%3A00%3A19&type=chart