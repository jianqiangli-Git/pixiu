'''
读取 json 文件模块，对 json 文件做一些预处理，比如读取为 pandas 格式，numpy 格式等
'''

import json
import os

cur_path = os.getcwd()
# find() 检测字符串中是否包含子字符串 str,如果指定 beg 和 end 范围，则检查是否包含在指定范围内，如果包含子字符串返回开始的索引值，否则返回-1
root_path = cur_path[:cur_path.find('pixiu') + len('pixiu')]
data_dir = root_path + os.sep + 'Crawller' + os.sep + 'result'
os.chdir(data_dir)

# path = r'C:\Users\lijianqiang\PycharmProjects\pixiu\Crawller\result\navStockDict.json'
# p = r'navStockDict.json'
def load_json(filename):
    '''
    :param filename: 要获取的文件名，只需要传入文件名即可，无需传入完整路径
    :return: dict 类型的数据
    '''
    try:
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print("some error occurred in JsonLoadApi.load_json")
        print(e)

# load_json(p)