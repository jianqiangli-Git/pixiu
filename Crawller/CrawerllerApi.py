'''
这个模块主要是用来存放数据源api
'''

# top 10 stock website
XQ_BASE = r'https://xueqiu.com/'
DFCF_BASE = r'https://stock.eastmoney.com/'
JCZX_BASE = r'http://www.cninfo.com.cn/'
LXLT_BASE = r'https://www.55188.com/'
THS_BASE = r'https://www.10jqka.com.cn/'
ZQSB_BASE = r'http://www.stcn.com/'

XQ_HQ = XQ_BASE + 'hq/'

#行业 url 类
class XQIndustryUrl():
    def __init__(self):
        self._base_url = XQ_HQ

    @property
    def url(self):
        return self._base_url

#指数 url 类
class XQIndexUrl():
    def __init__(self):
        self._base_url = XQ_BASE

    @property
    def url(self):
        return self._base_url

#雪球 行业下的股票url类
class XQStockUrl():
    def __init__(self,url):
        self._base_url = url

    @property
    def url(self):
        return self._base_url




