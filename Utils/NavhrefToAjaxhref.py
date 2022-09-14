'''
行业导航 url 转换为真实 ajax 的 url
'''
import time
from urllib.parse import parse_qs, urlsplit
from Crawller.CrawllerApi import XQ_SECOND_NAV_AJAX_BASE, XQ_THIRD_NAV_AJAX_BASE,XQ_ORDER_AJAX_BASE

# "https://xueqiu.com/hq/#exchange=HK&firstName=2&secondName=2_0"
# service/v5/stock/screener/quote/list?page={page}&size=30&order=desc&orderby=percent&order_by=percent&market={market}&type=sh_sz&_={t}
def secondNavhrefToAjaxhref(href, page, kind):
    ajax_url = XQ_SECOND_NAV_AJAX_BASE
    try:
        if href.startswith(('http://', 'https://')):
            t = int(time.time() * 1000)
            fragment = urlsplit(href).fragment
            qs = parse_qs(fragment)
            exchange = qs['exchange'][0]
            market = exchange
            # kind = 'sh_sz'
            ajax_url = ajax_url.format(page=page, market=market, kind=kind, t=t)
            # print(ajax_url)
            return ajax_url
        else:
            raise Exception("Url Invalid Error")
    except Exception as e:
        print('some error occurred in navhrefToAjaxhref')
        print(e)

# https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=30&order=desc&order_by=percent&exchange=US&market=US&ind_code=255030&_=1662779914175
# href:"https://xueqiu.com/hq/#exchange=US&plate=3_1_56&firstName=3&secondName=3_1&level2code=453010"
def thirdNavhrefToAjaxhref(href, page):
    ajax_url = XQ_THIRD_NAV_AJAX_BASE
    try:
        if href.startswith(('http://', 'https://')):
            t = int(time.time()*1000)
            fragment = urlsplit(href).fragment
            qs = parse_qs(fragment)
            exchange = qs['exchange'][0]
            market = exchange
            ind_code = qs['level2code'][0]
            ajax_url = ajax_url.format(page=page, exchange=exchange, market=market, ind_code=ind_code, t=t)
            # print(ajax_url)
            return ajax_url
        else:
            raise Exception("Url Invalid Error")
    except Exception as e:
        print('some error occurred in navhrefToAjaxhref')
        print(e)

#https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=30&order=desc&order_by=volume&exchange=CN&market=CN&type=sza&_=1663059410658
#  "href": "https://xueqiu.com/hq/#exchange=CN&plate=1_3_11&firstName=1&secondName=1_3&type=sza&order=desc&order_by=volume"
# 排行的href的ajax转换
def orderhrefToAjaxhref(href, page):
    ajax_url = XQ_ORDER_AJAX_BASE
    try:
        if href.startswith(('http://', 'https://')):
            t = int(time.time()*1000)
            fragment = urlsplit(href).fragment
            qs = parse_qs(fragment)
            exchange = qs['exchange'][0]
            market = exchange
            kind = qs['type'][0]
            order = qs['order'][0]
            order_by = qs['order_by'][0]
            ajax_url = ajax_url.format(page=page, exchange=exchange, market=market, kind=kind, order=order, order_by=order_by, t=t)
            return ajax_url
        else:
            raise Exception("Url Invalid Error")
    except Exception as e:
        print('some error occurred in orderhrefToAjaxhref')
        print(e)



# a = 'https://xueqiu.com/hq/#exchange=US&plate=3_1_56&firstName=3&secondName=3_1&level2code=453010'
# thirdNavhrefToAjaxhref(a,1)
# b = "https://xueqiu.com/hq/#exchange=HK&firstName=2&secondName=2_0"
# secondNavhrefToAjaxhref(b,1)
c = "https://xueqiu.com/hq/#exchange=CN&plate=1_3_11&firstName=1&secondName=1_3&type=sza&order=desc&order_by=volume"
# orderhrefToAjaxhref(c,1)
