'''
爬虫抽象基类的爬取模块的具体实现，不同类型的数据源api实现不同的爬取逻辑即可
'''
import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Crawller.CrawllerAbs import CrawllerBase
from Crawller.Parser import BSParser
from Utils.TimeConsumeStatisticer import asyncTimeConsume
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from DataSaver.JsonSaver.JsonSaveApi import save_to_json
from Crawller.ConstInfo import VOL_NAME,second_nav_kind
from Utils.NavhrefToAjaxhref import secondNavhrefToAjaxhref, thirdNavhrefToAjaxhref, orderhrefToAjaxhref
from Crawller.ConstInfo import headers
from math import ceil
import asyncio
import aiohttp
import traceback
import requests_html
from asyncio import Semaphore
import json

webdriver_location = r'C:\Users\lijianqiang\Desktop\chromedriver'
wait_time = 10
concurrency = 10
samphore = Semaphore(concurrency)

# 不同类别爬虫的基类
# 只有抽象基类，想要统一只是用抽象基类的 crawl 方法，那么就需要定义基类，让不同类别的爬虫类继承此基类，否则，抽象基类就要
# 定义不同的抽象方法，不同类别的爬虫类就都要实现所有抽象方法，显然不合适，而新基类继承抽象类，将统一的 crawl 交给不同爬虫子类进行不同实现
# 新基类可以实例化，通过新基类调用统一的 crawl 方法比较合适。
class CateCrawller(CrawllerBase):
    # requests_html 只创建一个全局 session 而不是每次请求都创建一个 session
    _requests_html_session = requests_html.AsyncHTMLSession()

    def __init__(self,cateUrl):
        '''
        :param cateUrl: 传入CrawerllerApi模块的 url类别对象，例如XQIndustry，XQIndex
        '''
        super(CateCrawller, self).__init__(cateUrl)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self._driver = webdriver.Chrome(service=Service(executable_path=webdriver_location), options=options)
        # print(self._driver.get_window_rect())
        # self._driver.set_window_position(x=600,y=9)
        self._wait = WebDriverWait(self._driver, timeout=wait_time)

    # 使用 requests_html 请求
    @staticmethod
    @asyncTimeConsume
    async def scrapyUrlByRequestsHtml(url,**kwargs):
        '''
        :param url: 请求 url
        :return: <class 'requests_html.HTML'>
        '''
        try:
            # async with samphore:
            content = await CateCrawller._requests_html_session.get(url)
            # render 用来渲染 js,sleep 指定渲染时间，这个时间不好设置
            await content.html.arender(retries=3,sleep=0.1)
            if 'callback' in kwargs:
                func = kwargs['callback']
                args = kwargs['args']
                func(args)
            return content.html
        except Exception as e:
            print("some error occured in scrapyUrlByRequestsHtml")
            print(e)
        # finally:
        #     await session.close()

    # 使用 selenium 请求
    @asyncTimeConsume
    async def scrapyUrlBySelenium(self,url):
        try:
            self._driver.get(url)
            # 显式等待，等到类似上证指数的元素出现即返回，否则超时抛出异常，超时时间由 wait_time 控制
            self._wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,'.StockSlider_type_pfC')))
            return self._driver.page_source
        except Exception as e:
            print("some error occured in scrapyUrlBySelenium")
            print(e)

    # 使用 aiohttp 请求
    @staticmethod
    async def scrapyUrlByAiohttp(url,cookies=True):
        async with samphore:
            # 此处频繁创建 session 请求主页又关闭，比较浪费资源，后续可优化为创建一个 session
            async with aiohttp.ClientSession(headers=headers) as session:
                if cookies:
                    await session.get('https://xueqiu.com/')  # 主要是用 session 管理 cookie 信息
                async with session.get(url) as resp:
                    content = await resp.text()
                    return content
            # 以下代码先请求 https://xueqiu.com/ 再请求 https://xueqiu.com/hq 没反应，但是请求 XQ_INDEXINFO_AJAX 就没问题
            # 现象就像是死循环，也没报异常，不明白怎么回事（可能是 access-allow-origin限制origin的原因），遂改为以上检查是否需要 cookies 先跑通
            # async with aiohttp.ClientSession(headers=headers) as s:
            #     await s.get("https://xueqiu.com/")
            #     resp = await s.get(url)
            #     text = await resp.text()
            #     # print(text)

#行业分类爬取类
class NavCrawller(CateCrawller):
    def __init__(self, cateUrl):
        super(NavCrawller, self).__init__(cateUrl)

    def _parse(self, content):
        nav = {}
        try:
            bs = BSParser(content)
            containers = bs._soup.find_all(attrs={'class': 'nav-container'})
            for container in containers:
                first_nav = container.find(attrs={'class': 'first-nav'})
                second_navs = container.find(attrs={'class': 'second-nav'}).contents
                first_nav_text = first_nav.select("span[class='name']")[0].text
                first_nav_dict = {}
                for second_nav in second_navs:
                    second_nav_dict = {}
                    second_nav_text = second_nav.find(text=True).get_text()  # 有文本的时候获取文本，而不继续向下获取子孙文本
                    child_webElements_of_li = second_nav.contents  # 列表形式
                    child_tags_of_li = [tag.name for tag in child_webElements_of_li]
                    second_nav_href = self._url + second_nav.a.attrs['href'] if 'a' in child_tags_of_li else 'No-href'
                    third_nav = second_nav.div.children if 'div' in child_tags_of_li else "NO-third-nav"
                    second_nav_dict['href'] = second_nav_href if second_nav_href != "No-href" else "No-href"
                    if third_nav != "NO-third-nav":
                        third_nav_dict = {}
                        count_of_li = 0  # 看一下 third 下的li有多少个，从而统计有多少个三级行业
                        for ul in third_nav:
                            li = ul.find_all('a')
                            count_of_li = count_of_li + len(li)
                            for a in li:
                                li_text = a['title']
                                li_href = self._url + a.get('href')
                                if li_text in third_nav_dict:  # 发现恒生行业有的有2个相同的行业
                                    third_nav_dict[li_text + '2'] = {'href': li_href}
                                else:
                                    third_nav_dict[li_text] = {'href': li_href}
                        second_nav_dict["third-nav"] = third_nav_dict
                    else:
                        second_nav_dict['third-nav'] = "NO-third-nav"
                    first_nav_dict[second_nav_text] = second_nav_dict
                nav[first_nav_text] = first_nav_dict
            print(nav)  # 获取一级标签、二级标签、三级标签及 href 的字典
            save_to_json(nav, 'navInfoDict.json', 'w')
            return nav
        except Exception as e:
            print("some error occured in NavCrawller._parse")
            print(e)

    async def requestDetailByAioHttp(self):
        print('requestDetailByAioHttp running')
        try:
            print(self._url)
            content = await self.scrapyUrlByAiohttp(self._url,cookies=False)
            nav = self._parse(content) #后续可以新开一个线程来处理解析，加快速度
            return nav
        except Exception as e:
            print("some error occured in NavCrawller.requestDetailByAioHttp")
            print(traceback.print_exc())

    def _crawl(self,*args,**kwargs):
        nav = {}
        print('NavCrawller running')
        self._driver.get(self._url)
        try:
            containers = self._wait.until(lambda d: d.find_elements(By.CLASS_NAME,"nav-container"))
            count = len(containers)
            for i in range(count):
                container = containers[i]
                # 将一级导航标签展开，否则无法获取二级标签
                self._driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", container, 'class', 'nav-container unfold')
                first_nav = container.find_element(By.CSS_SELECTOR,f".first-nav.nav{i}")
                second_navs = container.find_elements(By.CSS_SELECTOR,".second-nav>li")
                first_nav_dict = {}
                for second_nav in second_navs:
                    second_nav_dict = {}
                    second_nav_text = second_nav.text
                    child_webElements_of_li = second_nav.find_elements(By.XPATH,"./*")
                    child_tags_of_li = [tag.tag_name for tag in child_webElements_of_li]
                    second_nav_href = second_nav.find_element(By.TAG_NAME,"a").get_attribute('href') if 'a' in child_tags_of_li else 'No-href'
                    third_nav = second_nav.find_elements(By.CSS_SELECTOR,'.third-nav>ul') if 'div' in child_tags_of_li else "NO-third-nav" #third下的所有ul
                    second_nav_dict['href'] = second_nav_href if second_nav_href!= "No-href" else "No-href"
                    if (third_nav != "NO-third-nav"):
                        third_nav_dict = {}
                        count_of_li = 0 #看一下 third 下的li有多少个，从而统计有多少个三级行业
                        for ul in third_nav:
                            li = ul.find_elements(By.CSS_SELECTOR,'li a') #每个ul中，li 下的所有a标签元素
                            count_of_li = count_of_li +len(li)
                            for a in li:
                                li_text = a.get_attribute('title')
                                li_href = a.get_attribute('href')
                                if li_text in third_nav_dict: #发现恒生行业有的有2个相同的行业
                                    third_nav_dict[li_text+'2'] = {'href':li_href}
                                else:
                                    third_nav_dict[li_text] = {'href': li_href}
                        second_nav_dict["third-nav"] = third_nav_dict
                    else:
                        second_nav_dict['third-nav'] = "NO-third-nav"
                    first_nav_dict[second_nav_text] = second_nav_dict
                nav[first_nav.text] = first_nav_dict
            print(nav) #获取一级标签、二级标签、三级标签及 href 的字典
            return nav
        except NoSuchElementException as e:
            print("NavCrawller._crawl NoSuchElementException Occured")

#大盘指数爬取类
class IndexCrawller(CateCrawller):
    def __init__(self,cateUrl):
        super(IndexCrawller, self).__init__(cateUrl)

    async def requestDetailByAiohttp(self):
        print("requestDetailByAiohttp running(use async)")
        try:
            content = await self.scrapyUrlByAiohttp(self._url)
            content = json.loads(content)  # 将 str 转换为 dict
            items = content['data']['items']
            symbols = {}
            status_dict = {}
            for item in items:
                status_id = item['market']['status_id']
                status = item['market']['status']
                region = item['market']['region']
                symbol = item['quote']['symbol']
                code = item['quote']['code']
                exchange = item['quote']['exchange']
                name = item['quote']['name']
                symbols[symbol] = {'code': code, "exchange": exchange, 'name': name,'status_id':status_id,'status':status}
                status_dict[region] = {str(status_id):status}
            save_to_json(symbols, "indexSymbolDict.json", 'w')   # 将股市指数和代码的字典关系存为 json 文件
            save_to_json(status_dict, "statusDict.json", 'w')    # 将股市交易状态和代码的字典关系存为 json 文件
        except Exception as e:
            print("some error occured in IndexCrawller.requestDetailByAiohttp")
            print(traceback.print_exc())

    # html-requests 的异步请求
    @asyncTimeConsume
    async def requestDetailByRequestsHtml(self):
        try:
            print("requestDetailByRequestsHtml running(use async)")
            # <class 'requests_html.HTML'> 的信息都保存在 html 变量中，html.html获取 html 内容,html.find 查找元素，html.links 获取该页的所有链接
            html = await super(IndexCrawller, self).scrapyUrlByRequestsHtml(self._url)
            indexes = html.find(".StockSlider_home__stock-index__item_1V7")
            for index in indexes:  # 每分钟更新一次数据
                index_info = index.text
                print(index_info)
                print()
        except Exception as e:
            print("some error occured in IndexCrawller.requestDetailByRequestsHtml")
            print(traceback.print_exc())

    # selenium 的异步请求每页的详情
    @asyncTimeConsume
    async def requestDetailBySelenium(self):
        try:
            print("requestDetailBySelenium running(use async)")
            page = await self.scrapyUrlBySelenium(self._url)
            bs = BSParser(page)
            indexes = bs._soup.find_all(attrs={'class': 'StockSlider_home__stock-index__item_1V7'})
            for index in indexes:  # 每分钟更新一次数据
                index_info = index.text
                print(index_info)
                print()
        except Exception as e:
            print("some error occured in IndexCrawller.requestDetailBySelenium")
            print(traceback.print_exc())

        # headers = {  # httpx 的 client 不设置 user-agent 会发生 403 Forbidden
        #     'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/104.0.5112.102 Safari/537.36",
        #     'content-type': 'application/json, text/plain, */*'
        # }

        # async with httpx.AsyncClient(headers=headers) as client:
        #     r = await client.get(self._url)
        #     print(r.url)
        #     print("resp:")
        #     bs = BSParser(r.text)
        #     time.sleep(2)
        #     print(bs._soup.prettify())
        #     bs._soup.renderContents()
        #
        #     indexes = bs._soup.find_all(attrs={"name":"a","class":"StockSlider_home__stock-index__item_1V7"})
        #     print("index:",indexes)
        #     for index in indexes:  # 每分钟更新一次数据
        #         # index_info = index.get_text()  # eg:['上证指数', '3236.22', '-10.03(-0.31%)', '0']
        #         print(index)
        #         print()

        # async with samphore:
        #     async with aiohttp.ClientSession() as session:
        #         print(self._url)
        #         print("async==================")
        #         print(session.headers)
        #         for i in session.headers:
        #             print(i)
        #         async with session.get(self._url) as response:
        #             html = await response.text()
        #             print("Body:", html)

    def _crawl(self,*args,**kwargs):
        # 实验发现 useAsyncBySelenium 更快，三者时间分别为(1.29 vs 3.41 vs 5.94),事实证明：driver 第一次请求是最耗时间的，后面再用driver请求时间急剧减少
        if 'useAsyncBySelenium' in kwargs and kwargs['useAsyncBySelenium']:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.requestDetailBySelenium())
        elif 'useAsyncByRequestsHtml' in kwargs and kwargs['useAsyncByRequestsHtml']:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.requestDetailByRequestsHtml())
        elif 'useAsyncByAiohttp' in kwargs and kwargs['useAsyncByAiohttp']:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.requestDetailByAiohttp())
        else:
            try:
                print("IndexCrawller._crawl running(use sync)")
                self._driver.get(self._url)
                print(self._url)
                # 指定等待时间等待渲染（通常这个时间不好设置）
                # time.sleep(0.2)
                # 显式等待
                self._wait.until(lambda d: d.find_elements(By.CLASS_NAME, "StockSlider_type_pfC"))
                bs = BSParser(self._driver.page_source)
                indexes = bs._soup.find_all(attrs={'class':'StockSlider_home__stock-index__item_1V7'})
                for index in indexes: #每分钟更新一次数据
                    index_info = index.text.split('\n') #eg:['上证指数', '3236.22', '-10.03(-0.31%)', '0']
                    print(index_info)
                    print()
            except Exception as e:
                print("some error occured in IndexCrawller._crawl")
                print(e)

#股票信息爬取类:包括股票代码，当前价，涨跌幅，成交量，换手率
class StockInfoCrawller(CateCrawller):
    nav_stock_dict = {}

    def __init__(self,cateUrl):
        super(StockInfoCrawller, self).__init__(cateUrl)

    # 第一次改进:使用 aiohttp 异步时间:544.4213817119598(并发开到了6), 较之前使用selenium同步时间:1620.906483411789
    async def requestDetailByAioHttp(self,nav_type, nav):
        print("StockInfoCrawller.requestDetailByAioHttp running")
        volumn_name_dict = {}  # 建立股票各列英文名称和对应中文名称字典
        stocks_datails = {}  # 股票详情：股票代码，股票名称，当前价格，等
        columns = []
        size = 30
        try:
            if nav_type == 1:
                pass
            elif nav_type == 2:
                ajax = secondNavhrefToAjaxhref(self._url, 1, second_nav_kind[nav])
            elif nav_type == 3:
                ajax = thirdNavhrefToAjaxhref(self._url, 1)
            elif nav_type == 4:
                ajax = orderhrefToAjaxhref(self._url, 1)
            else:
                raise Exception("nav_type Error")
            content = await self.scrapyUrlByAiohttp(ajax, cookies=False)
            data = json.loads(content)['data']  # 将 str 转换为 dict
            total = data['count']
            pages = ceil(total/size) # size 是每页个数，total 是总数，从而获得页数
            # stocks = data['list']
            print(content)
            for page in range(pages):
                print("current page: ", page+1)
                # if page>8:
                #     continue
                if nav_type == 1:
                    pass
                elif nav_type == 2:
                    ajax = secondNavhrefToAjaxhref(self._url, page+1, second_nav_kind[nav])
                elif nav_type == 3:
                    ajax = thirdNavhrefToAjaxhref(self._url, page+1)
                elif nav_type == 4:
                    ajax = orderhrefToAjaxhref(self._url, page+1)
                else:
                    raise Exception("nav_type Error")
                print('ajax:',ajax)
                content = await self.scrapyUrlByAiohttp(ajax, cookies=False)
                data = json.loads(content)['data']  # 将 str 转换为 dict
                stocks = data['list']
                for stock in stocks:
                    temp = []
                    for vol in VOL_NAME.keys():
                        temp.append(stock[vol])
                    if temp[0] not in StockInfoCrawller.nav_stock_dict:
                        StockInfoCrawller.nav_stock_dict[temp[0]] = [nav]
                    else:
                        StockInfoCrawller.nav_stock_dict[temp[0]].append(nav)
                    print("tmp:", temp,'nav:',StockInfoCrawller.nav_stock_dict[temp[0]])
            print(StockInfoCrawller.nav_stock_dict)
            save_to_json(StockInfoCrawller.nav_stock_dict,'navStockDict.json','w') #将股票打上行业标签
        except Exception as e:
            print("some error occured in StockInfoCrawller.requestDetailByAioHttp")
            print(traceback.print_exc())

    def _crawl(self, *args, **kwargs):
        self._driver.get(self._url)
        print("StockInfoCrawller running")
        volumn_name_dict = {} #建立股票各列英文名称和对应中文名称字典
        stocks_datails = {} #股票详情：股票代码，股票名称，当前价格，等
        columns = []
        stockList_webElement = self._wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#stockList"))
        columns_webElement = stockList_webElement.find_elements(By.CSS_SELECTOR, "thead>tr>th")
        for column in columns_webElement:
            data_key = column.get_attribute('data-key')
            data_text = column.text
            volumn_name_dict[data_key] = data_text
        print("vol_name_dict:")
        print(volumn_name_dict)
        save_to_json(volumn_name_dict, 'volNameDict.json', 'w')
        pageList_webElement = self._wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#pageList"))
        while True:
            try:
                current_page = pageList_webElement.find_element(By.CLASS_NAME,'active').text if len(pageList_webElement.text)!=0 else 1
                print("current_page:",current_page)
                stockLists = stockList_webElement.find_elements(By.CSS_SELECTOR,'tbody>tr')
                for stock in stockLists:
                    stock_href = stock.find_element(By.CSS_SELECTOR,'td:first-child>a').get_attribute('href')
                    stock_info = stock.text.split(' ')
                    stock_info.append(stock_href)
                    print(stock_info)
                    stocks_datails[stock_info[0]] = stock_info[1:]
                next_page = pageList_webElement.find_element(By.CSS_SELECTOR,".next>a")
                self._driver.execute_script("arguments[0].click();",next_page) #点击 a 标签的方法
                time.sleep(1) #需要等待页面加载完成，可以 0.1
            except NoSuchElementException:
                print("no next page")
                print(stocks_datails)
                break
            except Exception as e:
                print("some errors occured in StockInfoCrawller._crawl!")
                print(e)



