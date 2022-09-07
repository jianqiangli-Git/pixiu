'''
爬虫运行主进程
'''
import asyncio
from Crawller.CrawllerApi import XQIndexUrl,XQIndustryUrl,XQStockUrl,XQNewIndexUrl
from Crawller.CrawllerAbs import CrawllerBase
from Crawller.CrawllerImp import CateCrawller,NavCrawller,IndexCrawller,StockInfoCrawller
import time
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
#
index = XQNewIndexUrl()
c = IndexCrawller(index)

async def test():
    index_tasks = [c.requestDetailByAiohttp() for _ in range(1)]
    await asyncio.gather(*index_tasks)

# async def main():
#     # global session
#     # session = requests_html.AsyncHTMLSession()
#     tasks = [c.requestDetail() for _ in range(1)]
#     await asyncio.gather(*tasks)

if __name__ == '__main__':
    t = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    print("use time ",time.time()-t)

# if __name__ == '__main__':
#     s2 = time.time()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
# #     # asyncio.run(main())
# #     # asyncio.run(c.requestDetail())
#     print(f"detail spend {time.time() - s2}")

# industry = XQIndustryUrl()
# n = NavCrawller(industry)
# industry = n.crawl()
# for first in industry:
#     if first in ["最近访问","香港股市","美国股市","债券及回购","基金","私募"]:
#         print(f'{first} pass...')
#         continue
#     for ins in industry[first]:
#         if industry[first][ins]["href"] != "No-href":
#             print(ins,"href:",industry[first][ins]["href"])
#             if ins in ["内部交易","私募中心","美股一览","明星股","新上市公司"]:
#                 continue
#             stocks = XQStockUrl(industry[first][ins]["href"])
#             s = StockInfoCrawller(stocks)
#             s.crawl()
#         elif industry[first][ins]["third-nav"] != "NO-third-nav":
#             print(ins,"third-nav:",industry[first][ins]["third-nav"])
#             for i in industry[first][ins]["third-nav"]:
#                 print(i,"href:",industry[first][ins]["third-nav"][i]["href"])
#                 stocks = XQStockUrl(industry[first][ins]["third-nav"][i]["href"])
#                 s = StockInfoCrawller(stocks)
#                 s.crawl()

# stock = XQStockUrl()
# s = StockInfoCrawller(stock)
# s.crawl()