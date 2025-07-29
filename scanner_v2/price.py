import requests
import urllib3
# 禁用 HTTPS 安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def do_scan():
  url = "https://scanner.tradingview.com/america/scan?label-product=popup-screener-stock"
  Cookie = '_ga=GA1.1.1233108505.1738595349; cookiesSettings={"analytics":true,"advertising":true}; cookiePrivacyPreferenceBannerProduction=accepted; theme=light; __gads=ID=e3d5adff96d0e7b4:T=1740316804:RT=1753061225:S=ALNI_MaAmyI4r-yviDtc506P4aWLFEsjJQ; __gpi=UID=00001048cbf5bdd0:T=1740316804:RT=1753061225:S=ALNI_MbIr5Z5Kmw6Qw8G7MAjrp4MWyMcbA; __eoi=ID=240fa7f019267950:T=1740316804:RT=1753061225:S=AA-AfjbJp4H6baKAFJLYgth0Fbct; device_t=VDYxeUJROjIsdVlqb0JROjEsOHNnWEJnOjEsWFpBWEJnOjIsRHROUkJnOjA.JoBF2Y1XC3b_-lZzEKKN7y8EFeboTIcqTffe85Q9tog; sessionid=csoqv9cplhmu4txhz0fzfxvkzc5ayfj3; sessionid_sign=v3:MIl9yy9hBAfhilIzrcG0gyzUpD+YVGfj+5SMnLsHqUI=; png=3f045c69-fd72-42a7-95d3-924c2cc6b302; etg=3f045c69-fd72-42a7-95d3-924c2cc6b302; cachec=3f045c69-fd72-42a7-95d3-924c2cc6b302; tv_ecuid=3f045c69-fd72-42a7-95d3-924c2cc6b302; _sp_ses.cf1a=*; _ga_YVVRYGL0E0=GS2.1.s1753495333$o1282$g1$t1753498694$j59$l0$h0; _sp_id.cf1a=417e44ab-7e61-4e3e-9886-7b243d437dfc.1731934501.143.1753500198.1753444988.6bcafd61-c647-4c9e-b31b-7a9c479abc3f.b9e2002d-3ce9-4886-a203-0ccc947a54e7.62ae606b-5866-4af6-895b-84eef0b5deb6.1753495333880.25'
  headers = {
    "Referer": "https://cn.tradingview.com/",
    'Cookie': Cookie,
    "Content-Type": "application/json"
  }

  payload = '{"columns":["name","description","logoid","update_mode","type","typespecs","premarket_change_from_open","close","pricescale","minmov","fractional","minmove2","currency","volume","premarket_change","relative_volume_10d_calc","float_shares_outstanding_current","exchange"],"filter":[{"left":"premarket_change_from_open","operation":"greater","right":15}],"ignore_unknown_fields":false,"options":{"lang":"zh"},"range":[0,100],"sort":{"sortBy":"premarket_change_from_open","sortOrder":"desc"},"symbols":{},"markets":["america"],"filter2":{"operator":"and","operands":[{"operation":{"operator":"or","operands":[{"operation":{"operator":"and","operands":[{"expression":{"left":"type","operation":"equal","right":"stock"}},{"expression":{"left":"typespecs","operation":"has","right":["common"]}}]}},{"operation":{"operator":"and","operands":[{"expression":{"left":"type","operation":"equal","right":"stock"}},{"expression":{"left":"typespecs","operation":"has","right":["preferred"]}}]}},{"operation":{"operator":"and","operands":[{"expression":{"left":"type","operation":"equal","right":"dr"}}]}},{"operation":{"operator":"and","operands":[{"expression":{"left":"type","operation":"equal","right":"fund"}},{"expression":{"left":"typespecs","operation":"has_none_of","right":["etf"]}}]}}]}}]}}'

  response = requests.post(
    url, 
    headers=headers, 
    data=payload,
    verify=False
  )
  if response.status_code == 200:
    res = response.json()
    res_data = []
    for item in res['data']:
      d = item['d']
      stock_obj = {
        'code': d[0],
        'no_delay': d[3] == 'streaming',
        'change': "{:.2f}".format(d[6]) + '%',
      }
      res_data.append(stock_obj)
    # return [res_data[0]]
    return res_data

if __name__ == "__main__":
  data = do_scan()
  print(data)