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
from DataSaver.JsonSaver.JsonLoadApi import load_json
import requests_html

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

async def indexCrawllerTask():
    # index = XQNewIndexUrl()
    # ic = IndexCrawller(index)
    await ic.crawl(useAsyncByAiohttp=True)
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

async def navCrawllerTask():
    await nc.crawl(useAsyncByAiohttp=True)
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

async def stockCrawllerTask(industry):

    def stockMap(navUrlTuple):
        third = navUrlTuple[0]
        url = navUrlTuple[1]['href']
        sc = StockInfoCrawller(XQStockUrl(url))
        nav_type = 3 if second != '排行' else 4
        return asyncio.ensure_future(sc.requestDetailByAioHttp(nav_type, third))

    tasks = []
    for first in industry:
        if first in ["最近访问", "香港股市", "美国股市", "债券及回购", "基金", "私募"]:
            print(f'{first} pass...')
            continue
        for second in industry[first]:
            if second in ["内部交易", "新股上市", "龙虎榜", 'AH股溢价']:
                continue
            if industry[first][second]["href"] != "No-href":
                # print(second, "href:", industry[first][second]["href"])
                stocks = XQStockUrl(industry[first][second]["href"])
                s = StockInfoCrawller(stocks)
                tasks.append(asyncio.ensure_future(s.requestDetailByAioHttp(2, second)))
                # await s.requestDetailByAioHttp(2, second)
            if industry[first][second]["third-nav"] != "NO-third-nav":
                print(second, "third-nav:", industry[first][second]["third-nav"])
                # navUrlTuple = list(zip(industry[first][second]["third-nav"].keys(), industry[first][second]["third-nav"].values()))
                # tasks += list(map(stockMap, navUrlTuple))
                for third in industry[first][second]["third-nav"]:
                    # print(third, "href:", industry[first][second]["third-nav"][third]["href"])
                    stocks = XQStockUrl(industry[first][second]["third-nav"][third]["href"])
                    s = StockInfoCrawller(stocks)
                    nav_type = 3 if second != '排行' else 4
                    # await s.requestDetailByAioHttp(nav_type,third)
                    tasks.append(asyncio.ensure_future(s.requestDetailByAioHttp(nav_type, third)))
    # 第三次改进，异步爬取每个行业信息，总耗时:483
    print("task_len:", len(tasks))
    await asyncio.gather(*tasks)

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

async def run():
    tasks = [indexCrawllerTask(), navCrawllerTask()]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    t = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    print("=============================")
    t1 = time.time()
    navInfoDict = 'navInfoDict.json'
    industry = load_json(navInfoDict)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stockCrawllerTask(industry))
    save_to_json(StockInfoCrawller.nav_stock_dict, 'navStockDict.json', mode='w')  # 将股票打上行业标签
    save_to_csv(StockInfoCrawller.stocksList, 'stocks.csv', mode='a')    #将股票数据存为 csv
    print("run use time ", t1 - t)
    print("stock use time ", time.time()-t1)
    print("total time use ", time.time()-t)

