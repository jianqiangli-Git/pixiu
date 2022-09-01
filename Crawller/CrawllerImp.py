'''
爬虫抽象基类的爬取模块的具体实现，不同类型的数据源api实现不同的爬取逻辑即可
'''
import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Crawller.CrawllerAbs import CrawllerBase

# 不同类别爬虫的基类
# 只有抽象基类，想要统一只是用抽象基类的 crawl 方法，那么就需要定义基类，让不同类别的爬虫类继承此基类，否则，抽象基类就要
# 定义不同的抽象方法，不同类别的爬虫类就都要实现所有抽象方法，显然不合适，而新基类继承抽象类，将统一的 crawl 交给不同爬虫子类进行不同实现
# 新基类可以实例化，通过新基类调用统一的 crawl 方法比较合适。
class CateCrawller(CrawllerBase):
    def __init__(self,cateUrl):
        '''
        :param cateUrl: 传入CrawerllerApi模块的 url类别对象，例如XQIndustry，XQIndex
        '''
        super(CateCrawller, self).__init__(cateUrl)

#行业分类爬取类
class NavCrawller(CateCrawller):
    def __init__(self,cateUrl):
        super(NavCrawller, self).__init__(cateUrl)

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
                print(first_nav.text)
                print('============')
                first_nav_dict = {}
                for second_nav in second_navs:
                    second_nav_dict = {}
                    second_nav_text = second_nav.text
                    child_webElements_of_li = second_nav.find_elements(By.XPATH,"./*")
                    child_tags_of_li = [tag.tag_name for tag in child_webElements_of_li]
                    second_nav_href = second_nav.find_element(By.TAG_NAME,"a").get_attribute('href') if 'a' in child_tags_of_li else 'No-href'
                    third_nav = second_nav.find_elements(By.CSS_SELECTOR,'.third-nav>ul') if 'div' in child_tags_of_li else "NO-third-nav" #third下的所有ul
                    second_nav_dict['href'] = second_nav_href if second_nav_href!= "No-href" else "No-href"
                    # print(second_nav_text," ",child_tags_of_li,second_nav_href,third_nav)
                    if (third_nav != "NO-third-nav"):
                        third_nav_dict = {}
                        count_of_li = 0 #看一下 third 下的li有多少个，从而统计有多少个三级行业
                        for ul in third_nav:
                            li = ul.find_elements(By.CSS_SELECTOR,'li a') #每个ul中，li 下的所有a标签元素
                            count_of_li = count_of_li +len(li)
                            for a in li:
                                li_text = a.get_attribute('title')
                                li_href = a.get_attribute('href')
                                # print(li_text, " ", li_href)
                                if li_text in third_nav_dict: #发现恒生行业有的有2个相同的行业
                                    third_nav_dict[li_text+'2'] = {'href':li_href}
                                else:
                                    third_nav_dict[li_text] = {'href': li_href}
                        # print("len:",count_of_li)
                        # print(len(third_nav_dict)," third-nav-dict:",third_nav_dict)
                        second_nav_dict["third-nav"] = third_nav_dict
                    else:
                        second_nav_dict['third-nav'] = "NO-third-nav"
                    first_nav_dict[second_nav_text] = second_nav_dict
                # print("first-nav-dict",first_nav_dict)
                # print()
                nav[first_nav.text] = first_nav_dict
            print(nav) #获取一级标签、二级标签、三级标签及 href 的字典
            return nav
        except NoSuchElementException as e:
            print("NavCrawller._crawl NoSuchElementException occured")

#大盘指数爬取类
class IndexCrawller(CateCrawller):
    def __init__(self,cateUrl):
        super(IndexCrawller, self).__init__(cateUrl)

    def _crawl(self,*args,**kwargs):
        self._driver.get(self._url)
        print("IndexCrawller running")
        time.sleep(2)
        indexes = self._wait.until(lambda d: d.find_elements(By.CLASS_NAME, "StockSlider_home__stock-index__item_1V7"))
        for index in indexes: #每分钟更新一次数据
            index_info = index.text.split('\n') #eg:['上证指数', '3236.22', '-10.03(-0.31%)', '0']
            print(index_info)
            print()

#股票信息爬取类:包括股票代码，当前价，涨跌幅，成交量，换手率
class StockInfoCrawller(CrawllerBase):
    def __init__(self,cateUrl):
        super(StockInfoCrawller, self).__init__(cateUrl)

    def _crawl(self,*args,**kwargs):
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
        print(volumn_name_dict)
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
                print("some errors occured!")
                print(e)

