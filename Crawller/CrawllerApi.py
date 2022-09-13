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
# 所有10个指数的详细信息：name，symbol，market，exchange，open，current，high，low 等
XQ_INDEXINFO_AJAX = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=SH000001,SZ399001,SZ399006,SH000688,HKHSI,HKHSCEI,HKHSCCI,.DJI,.IXIC,.INX'
# 分钟级指数
XQ_INDEX_MINUTE_AJAX = 'https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol=SH000001&period=1d'
# 秒级指数
XQ_INDEX_SECOND_AJAX = r'https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH000001,SZ399001,SZ399006,SH000688&_= timestamp'
# 二级行业股票详情[沪深一览...](事实上&market也可以省略，重要的是type)
XQ_SECOND_NAV_AJAX_BASE = XQ_BASE + r'service/v5/stock/screener/quote/list?page={page}&size=30&order=desc&orderby=percent&order_by=percent&market={market}&type={kind}&_={t}'
# 三级行业股票详情
XQ_THIRD_NAV_AJAX_BASE = XQ_BASE + r'service/v5/stock/screener/quote/list?page={page}&size=30&order=desc&order_by=percent&exchange={exchange}&market={market}&ind_code={ind_code}&_={t}'
# 香港新股上市
# service/v5/stock/preipo/hk/query?page=1&size=30&order=desc&order_by=percent&type=unlisted&is_delay=true&_=1662978454699
#新股申购
XQ_NEW_STOCK_SUBSCRIPTION_AJAX_BAZE = XQ_BASE + r'service/v5/stock/preipo/cn/query?order_by=list_date&order=desc&page=1&size=10&type=income&_=1662956190070'
# 新股行情
XQ_NEW_STOCK_MARKET_AJAX_BASE = XQ_BASE + r'service/v5/stock/preipo/cn/query?order_by=list_date&order=desc&type=quote&page=1&size=10&_=1662956190069'
# 打新收益
XQ_NEW_STOCK_PROFIT_AJAX_BASE = XQ_BASE + r'service/v5/stock/preipo/cn/query?order_by=list_date&order=desc&page=1&size=10&type=income&_=1662956190070'
# 新股数据解析
XQ_NEW_STOCK_ANALYSE_AJAX_BASE = XQ_BASE + r'service/v5/stock/preipo/cn/query?order_by=list_date&order=desc&type=quote&page=1&size=30&_=1662956190072'


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




