'''
爬虫抽象基类模块，方便正式爬取模块的统一调用
'''
import time
import six
from abc import ABCMeta,abstractmethod

class CrawllerBase(six.with_metaclass(ABCMeta)):
    def __init__(self, cateUrl):
        '''
        :param cateUrl: 传入CrawerllerApi模块的 url类别对象，例如XQIndustry，XQIndex
        '''
        self._url = cateUrl.url

    @abstractmethod
    def _crawl(self,*args,**kwargs):
        pass

    #category 指明爬的内容，比如行业，大盘指数
    def crawl(self,*args,**kwargs):
        result = self._crawl(*args,**kwargs)
        # content = crawller(*args,**kwargs)
        print("Crawller received!")
        return result




