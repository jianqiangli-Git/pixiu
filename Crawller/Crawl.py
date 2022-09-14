'''
爬虫运行主进程
'''
import asyncio
from Crawller.CrawllerApi import XQIndexUrl, XQIndustryUrl, XQStockUrl, XQNewIndexUrl
from Crawller.CrawllerAbs import CrawllerBase
from Crawller.ConstInfo import second_nav_kind
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
c = IndexCrawller(index)
# s4 = time.time()
# for i in range(1):
#     c.crawl(useAsyncByAiohttp=True)
# print(f"requestsHtml spend {time.time() - s4}")

async def test():
    index_tasks = [c.requestDetailByAiohttp() for _ in range(10)]
    await asyncio.gather(*index_tasks)

# async def main():
#     # global session
#     # session = requests_html.AsyncHTMLSession()
#     tasks = [c.requestDetail() for _ in range(1)]
#     await asyncio.gather(*tasks)

# if __name__ == '__main__':
#     s2 = time.time()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(test())
# #     # asyncio.run(main())
# #     # asyncio.run(c.requestDetail())
#     print(f"detail spend {time.time() - s2}")

industry = XQIndustryUrl()
n = NavCrawller(industry)
# t1 = time.time()
# n.crawl()
# print("crawl use time ",time.time()-t1)

if __name__ == '__main__':
    t = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(n.requestDetailByAioHttp())
    print("requestDetailByAioHttp use time ", time.time()-t)

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

async def testindus():
    for first in industry:
        if first in ["最近访问", "香港股市", "美国股市", "债券及回购", "基金", "私募"]:
            print(f'{first} pass...')
            continue
        for second in industry[first]:
            if second in ["内部交易", "新股上市", "龙虎榜", 'AH股溢价']:
                continue
            if industry[first][second]["href"] != "No-href":
                print(second, "href:", industry[first][second]["href"])
                stocks = XQStockUrl(industry[first][second]["href"])
                s = StockInfoCrawller(stocks)
                await s.requestDetailByAioHttp(2, second)
            if industry[first][second]["third-nav"] != "NO-third-nav":
                print(second, "third-nav:", industry[first][second]["third-nav"])
                for third in industry[first][second]["third-nav"]:
                    print(third, "href:", industry[first][second]["third-nav"][third]["href"])
                    stocks = XQStockUrl(industry[first][second]["third-nav"][third]["href"])
                    s = StockInfoCrawller(stocks)
                    nav_type = 3 if second != '排行' else 4
                    await s.requestDetailByAioHttp(nav_type,third)

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
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(test_stock())