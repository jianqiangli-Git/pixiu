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
XQ_INDEX_MINUTE_AJAX = 'https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol=SH000001&period=1d'
XQ_INDEXINFO_AJAX = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=SH000001,SZ399001,SZ399006,SH000688,HKHSI,HKHSCEI,HKHSCCI,.DJI,.IXIC,.INX'
# quotec.json?symbol=HKHSI,HKHSCEI,HKHSCCI&_=1662602645982
XQ_INDEX_SECOND_AJAX = r'https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH000001,SZ399001,SZ399006,SH000688&_= timestamp'

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

#雪球 行业下的股票url类
class XQNewIndexUrl():
    def __init__(self):
        self._base_url = XQ_INDEXINFO_AJAX

    @property
    def url(self):
        return self._base_url




