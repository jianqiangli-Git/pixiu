'''
爬虫运行主进程
'''
import asyncio
from Crawller.CrawllerApi import XQIndexUrl, XQIndustryUrl, XQStockUrl, XQNewIndexUrl
from Crawller.CrawllerAbs import CrawllerBase
from Crawller.ConstInfo import second_nav_kind
from DataSaver.CSVSaver.CSVSaveApi import save_to_csv
from DataSaver.JsonSaver.JsonSaveApi import save_to_json
from Utils.NavhrefToAjaxhref import secondNavhrefToAjaxhref, thirdNavhrefToAjaxhref
from Crawller.CrawllerImp import CateCrawller, NavCrawller, IndexCrawller, StockInfoCrawller
import time
import os
import traceback
from collections import ChainMap
from asyncio import Semaphore
from multiprocessing import cpu_count, Queue
from concurrent.futures import ProcessPoolExecutor
from DataSaver.JsonSaver.JsonLoadApi import load_json
import requests_html
from multiprocessing import Manager

cpuCores = cpu_count()
cpuAvailable = cpuCores * 2 - 1
poolCapacity = cpuAvailable
concurrency = 10

# index = XQIndexUrl()
# c = IndexCrawller(index)
#
# s2 = time.time()
# c.crawl(useAsyncBySelenium=True)
# print(f"selenium spend {time.time() - s2}")
# print('===========================================')
#
# s1 = time.time()
# c.crawl()
# print(f"c spend {time.time() - s1}")
# print('===========================================')
#
# s3 = time.time()
# for i in range(1):
#     c.crawl(useAsyncByRequestsHtml=True)
# print(f"requestsHtml spend {time.time() - s3}")
# print("===========================================")
index = XQNewIndexUrl()
ic = IndexCrawller(index)


# s4 = time.time()
# for i in range(1):
#     c.crawl(useAsyncByAiohttp=True)
# print(f"requestsHtml spend {time.time() - s4}")

async def indexCrawllerTask(sem):
    # index = XQNewIndexUrl()
    # ic = IndexCrawller(index)
    await ic.crawl(useAsyncByAiohttp=True,sem=sem)
    # await asyncio.gather(*index_tasks)


# 使用 requests-html 异步获取 index 数据
# async def main():
#     # global session
#     # session = requests_html.AsyncHTMLSession()
#     tasks = [c.requestDetail() for _ in range(1)]
#     await asyncio.gather(*tasks)

# if __name__ == '__main__':
#     s2 = time.time()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(indexCrawllerTask())
# #     # asyncio.run(main())
# #     # asyncio.run(c.requestDetail())
#     print(f"detail spend {time.time() - s2}")

industry = XQIndustryUrl()
nc = NavCrawller(industry)


async def navCrawllerTask(sem):
    await nc.crawl(useAsyncByAiohttp=True,sem=sem)
    # await asyncio.gather(*nav_tasks)


# t1 = time.time()
# n.crawl()
# print("crawl use time ",time.time()-t1)

# if __name__ == '__main__':
#     t = time.time()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(n.requestDetailByAioHttp())
#     print("requestDetailByAioHttp use time ", time.time()-t)

'''
# 获取股票各列英文名称和对应中文名称字典volNameDict，在ConstInfo中有备份，如果页面结构有更新比如新增了列，可以执行此方法重新获取
stocks = XQStockUrl()
s = StockInfoCrawller(stocks)
s.getVolNameDict()
'''


# navInfoDict = 'navInfoDict.json'
# industry = load_json(navInfoDict)
# t1 = time.time()
# for first in industry:
#     if first in ["最近访问", "香港股市", "美国股市", "债券及回购", "基金", "私募"]:
#         print(f'{first} pass...')
#         continue
#     for second in industry[first]:
#         if second in ["内部交易", "私募中心", "美股一览", "明星股", "新上市公司", "新股上市", "龙虎榜", 'AH股溢价']:
#             continue
#         if industry[first][second]["href"] != "No-href":
#             print(second, "href:", industry[first][second]["href"])
#             stocks = XQStockUrl(industry[first][second]["href"])
#             s = StockInfoCrawller(stocks)
#             s.crawl()
#         elif industry[first][second]["third-nav"] != "NO-third-nav":
#             print(second,"third-nav:",industry[first][second]["third-nav"])
#             for i in industry[first][second]["third-nav"]:
#                 print(i,"href:",industry[first][second]["third-nav"][i]["href"])
#                 stocks = XQStockUrl(industry[first][second]["third-nav"][i]["href"])
#                 s = StockInfoCrawller(stocks)
#                 s.crawl()
# t2 = time.time()-t1

def stockCrawllerTask(industry):
    def stockMap(navUrlTuple):
        third = navUrlTuple[0]
        url = navUrlTuple[1]['href']
        sc = StockInfoCrawller(XQStockUrl(url))
        nav_type = 3 if second != '排行' else 4
        return asyncio.ensure_future(sc.requestDetailByAioHttp(nav_type, third))

    tasks = []
    href = []
    for first in industry:
        if first in ["最近访问", "香港股市", "美国股市", "债券及回购", "基金", "私募"]:
            print(f'{first} pass...')
            continue
        for second in industry[first]:
            if second in ["内部交易", "新股上市", "龙虎榜", 'AH股溢价']:
                continue
            if industry[first][second]["href"] != "No-href":
                print(second, "href:", industry[first][second]["href"])
                # stocks = XQStockUrl(industry[first][second]["href"])
                href.append((2,second,industry[first][second]["href"]))
                # s = StockInfoCrawller(stocks)
                # tasks.append(asyncio.ensure_future(s.requestDetailByAioHttp(2, second,sem)))
                # await s.requestDetailByAioHttp(2, second)
            if industry[first][second]["third-nav"] != "NO-third-nav":
                print(second, "third-nav:", industry[first][second]["third-nav"])
                # navUrlTuple = list(zip(industry[first][second]["third-nav"].keys(), industry[first][second]["third-nav"].values()))
                # tasks += list(map(stockMap, navUrlTuple))
                for third in industry[first][second]["third-nav"]:
                    print(third, "href:", industry[first][second]["third-nav"][third]["href"])
                    # stocks = XQStockUrl(industry[first][second]["third-nav"][third]["href"])
                    # s = StockInfoCrawller(stocks)
                    nav_type = 3 if second != '排行' else 4
                    href.append((nav_type, third, industry[first][second]["third-nav"][third]["href"]))
                    # await s.requestDetailByAioHttp(nav_type,third)
                    # tasks.append(asyncio.ensure_future(s.requestDetailByAioHttp(nav_type, third,sem)))
    # 第三次改进，异步爬取每个行业信息，总耗时:483
    print("task_len:", len(tasks))
    # return href,tasks
    return href
    # await asyncio.gather(*tasks)


# if __name__ == '__main__':
#     t3 = time.time()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(testindus())
#     t4 = time.time()-t3
#     print("fisrt stock use ",t2)
#     print("second stock use ",t4)


# stock = XQStockUrl('https://xueqiu.com/hq/#exchange=US&plate=3_1_30&firstName=3&secondName=3_1&level2code=255030')
# s = StockInfoCrawller(stock)
#
# async def test_stock():
#     task = [asyncio.create_task(s.requestDetailByAioHttp())]
#     await asyncio.gather(*task)
#

async def amain():
    sem = Semaphore(concurrency)
    tasks = [indexCrawllerTask(sem), navCrawllerTask(sem)]
    await asyncio.gather(*tasks)


# def main():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(amain())

async def taksrun(tas, ind, step, task_e, LOCK, nav_stock_dict, stocksDict):
    try:
        sem = Semaphore(concurrency)
        start = ind * step
        end = min(start + step, task_e)
        hrefs = tas[start:end]
        print("current process ", os.getpid(), " and tasks[", start, ":", end, "]")

        def createTask(href):
            nav_type = href[0]
            label = href[1]
            url = href[2]
            stocks = XQStockUrl(url)
            stockSpider = StockInfoCrawller(stocks)
            return asyncio.ensure_future(stockSpider.requestDetailByAioHttp(nav_type, label, sem, LOCK, nav_stock_dict, stocksDict))

        tsks = map(createTask, hrefs)    #只需要定义每个元素的处理方式，自己会返回包含处理好元素的列表

        # for stock in stocks:
        #     nav_type = stock[0]
        #     label = stock[1]
        #     url = stock[2]
        #     s = StockInfoCrawller(url)
        #     tsks.append(asyncio.ensure_future(s.requestDetailByAioHttp(nav_type, label, sem, LOCK, nav_stock_dict, stocksDict)))
        await asyncio.gather(*tsks)
    except Exception as error:
        print('some error occurred in taksrun')
        print(error)

def callbak(res):
    #ProcessPoolExecutor会将异常封装到futures对象中，需要调用.exception()方法获取异常
    exception = res.exception()
    if exception:
        # 如果exception获取到了值，说明有异常.exception就是异常类
        print("callback: ",exception)

def run(tas, ind, step, task_e, LOCK, nav_stock_dict, stocksDict):
    try:
        print('-------------------------------------------')
        print("current process:", os.getpid(), " is running")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(taksrun(tas, ind, step, task_e, LOCK, nav_stock_dict, stocksDict))
        # loo = asyncio.get_event_loop()
        # loo.run_until_complete(taksrun(tas, ind, step, task_e))
        loop.close()
    except Exception as error:
        print('some error occurred in run')
        print(traceback.format_exc())


if __name__ == '__main__':
    results = []
    t = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
    print("=============================")
    t1 = time.time()
    queue = Queue()
    navInfoDict = 'navInfoDict.json'
    industry = load_json(navInfoDict)
    # tasks,href = stockCrawllerTask(industry,)
    hrefs = stockCrawllerTask(industry)
    print("get tasks:", hrefs[0], type(hrefs[0]))
    task_end = len(hrefs) - 1
    print('tasks len:', len(hrefs))
    eachCoreTasks = len(hrefs) // cpuCores
    print('eachCoreTask:', eachCoreTasks)
    nav_stock_dict = Manager().dict()  #{stock:nav} 的字典
    stocksDict = Manager().dict()      #{stock:[stock详情,[nav1,nav2]]} 的字典
    LOCK = Manager().Lock()
    try:
        # 第四次改进:使用进程池多进程运行，使用 Manage 管理共享变量，程序总耗时:104
        with ProcessPoolExecutor(cpuAvailable) as excutor:
            # ts = excutor.map(run, range(cpuAvailable))
            # 多进程要考虑变量共享的问题
            for index in range(cpuCores+1):
                print("index:", index)
                result = excutor.submit(run, hrefs, index, eachCoreTasks, task_end, LOCK, nav_stock_dict, stocksDict).add_done_callback(callbak)
                results.append(result)

        # for result in results:
        #     r = result.result()
        #     print("r:", r)
    except Exception as e:
        print("some error occurred in main")
        print(traceback.format_exc())

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(stockCrawllerTask(industry))
    print('nav_stock_dict============')
    print(nav_stock_dict)
    print('stocksDict==============')
    print(stocksDict)
    save_to_json(dict(nav_stock_dict), 'navStockDict.json', mode='w')  # 将股票打上行业标签,<class 'multiprocessing.managers.DictProxy'>需要转换为dict才能存为json，否则不能序列化
    save_to_csv(stocksDict.values(), f'stocks{int(time.time())}.csv', mode='a')  # 将股票数据存为 csv
    print("run use time ", t1 - t)
    print("stock use time ", time.time() - t1)
    print("total time use ", time.time() - t)
