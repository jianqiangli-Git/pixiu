'''
爬虫运行主进程
'''

from Crawller.CrawerllerApi import XQIndexUrl,XQIndustryUrl,XQStockUrl
from Crawller.CrawllerAbs import CrawllerBase
from Crawller.CrawllerImp import CateCrawller,NavCrawller,IndexCrawller,StockInfoCrawller


# index = XQIndexUrl()
# c = IndexCrawller(index)
# c.crawl()

industry = XQIndustryUrl()
n = NavCrawller(industry)
industry = n.crawl()
for first in industry:
    if first in ["最近访问","香港股市","美国股市","债券及回购","基金","私募"]:
        print(f'{first} pass...')
        continue
    for ins in industry[first]:
        if industry[first][ins]["href"] != "No-href":
            print(ins,"href:",industry[first][ins]["href"])
            if ins in ["内部交易","私募中心","美股一览","明星股","新上市公司"]:
                continue
            stocks = XQStockUrl(industry[first][ins]["href"])
            s = StockInfoCrawller(stocks)
            s.crawl()
        elif industry[first][ins]["third-nav"] != "NO-third-nav":
            print(ins,"third-nav:",industry[first][ins]["third-nav"])
            for i in industry[first][ins]["third-nav"]:
                print(i,"href:",industry[first][ins]["third-nav"][i]["href"])
                stocks = XQStockUrl(industry[first][ins]["third-nav"][i]["href"])
                s = StockInfoCrawller(stocks)
                s.crawl()

# stock = XQStockUrl()
# s = StockInfoCrawller(stock)
# s.crawl()