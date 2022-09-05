'''
统计函数运行耗时装饰器
'''
import time

#异步函数装饰器
def asyncTimeConsume(func):
    async def innerFun(*args,**kwargs):
        t = time.time()
        result = await func(*args,**kwargs)
        print(f"{func.__name__} func consume time {time.time()-t}")
        return result
    return innerFun

#普通函数装饰器
def timeConsume(func):
    def innerFun(*args,**kwargs):
        t = time.time()
        result = func(*args,**kwargs)
        print(f"{func.__name__} func consume time {time.time()-t}")
        return result
    return innerFun