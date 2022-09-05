'''
爬虫抽象基类模块，方便正式爬取模块的统一调用
'''
import time
import six
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from abc import ABCMeta,abstractmethod
from asyncio import Semaphore


webdriver_location = r'C:\Users\lijianqiang\Desktop\chromedriver'
wait_time = 6
concurrency = 4
samphore = Semaphore(concurrency)

class CrawllerBase(six.with_metaclass(ABCMeta)):
    def __init__(self,cateUrl):
        '''
        :param cateUrl: 传入CrawerllerApi模块的 url类别对象，例如XQIndustry，XQIndex
        '''
        self._url = cateUrl.url
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self._driver = webdriver.Chrome(service=Service(executable_path=webdriver_location),options=options)
        # print(self._driver.get_window_rect())
        # self._driver.set_window_position(x=600,y=9)
        self._wait = WebDriverWait(self._driver,timeout=wait_time)

    @abstractmethod
    def _crawl(self,*args,**kwargs):
        pass

    #category 指明爬的内容，比如行业，大盘指数
    def crawl(self,*args,**kwargs):
        result = self._crawl(*args,**kwargs)
        # content = crawller(*args,**kwargs)
        print("Crawller received!")
        return result




