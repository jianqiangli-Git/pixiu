'''
保存一些静态信息
'''
symbol = {
    'SH000001': {'code': '000001', 'exchange': 'SH', 'name': '上证指数'},
    'SZ399001': {'code': '399001', 'exchange': 'SZ', 'name': '深证成指'},
    'SZ399006': {'code': '399006', 'exchange': 'SZ', 'name': '创业板指'},
    'SH000688': {'code': '000688', 'exchange': 'SH', 'name': '科创50'},
    'HKHSI': {'code': 'HSI', 'exchange': 'HK', 'name': '恒生指数'},
    'HKHSCEI': {'code': 'HSCEI', 'exchange': 'HK', 'name': '国企指数'},
    'HKHSCCI': {'code': 'HSCCI', 'exchange': 'HK', 'name': '红筹指数'},
    '.DJI': {'code': '.DJI', 'exchange': 'INDEXDJX', 'name': '道琼斯指数'},
    '.IXIC': {'code': '.IXIC', 'exchange': 'NASDAQ', 'name': '纳斯达克综合指数'},
    '.INX': {'code': '.INX', 'exchange': 'INDEXSP', 'name': '标普500指数'},
}

# 股票列表各列英文名称和对应中文名称字典
VOL_NAME = {
  "symbol": "股票代码",
  "name": "股票名称",
  "current": "当前价",
  "chg": "涨跌额",
  "percent": "涨跌幅",
  "current_year_percent": "年初至今",
  "volume": "成交量",
  "amount": "成交额",
  "turnover_rate": "换手率",
  "pe_ttm": "市盈率(TTM)",
  "dividend_yield": "股息率",
  "market_capital": "市值",
  "has_follow": "操作"
}

# 二级行业及其对应type字典
second_nav_kind = {
    '沪深一览': 'sh_sz',
    '科创板': 'kcb',
    '港股一览': 'hk',
    '美股一览': 'us',
    '明星股': 'us_star',
    '中国概念股': 'us_china',
    '上市预告': 'unlisted',
    '新上市公司': 'listed',
}

'''
amount:成交额'
volumn:成交量
'''

headers = {  # httpx、aiohttp 的 client 不设置 user-agent 会发生 403 Forbidden，aiohttp 不设置 cookie 会发生 400 错误
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    'Origin': "https://xueqiu.com"
    # 'content-type': 'application/json, text/plain, */*',
}