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

headers = {  # httpx、aiohttp 的 client 不设置 user-agent 会发生 403 Forbidden，aiohttp 不设置 cookie 会发生 400 错误
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    'Origin': "https://xueqiu.com"
    # 'content-type': 'application/json, text/plain, */*',
}