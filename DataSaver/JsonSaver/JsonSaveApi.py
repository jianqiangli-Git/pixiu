'''
将数据存储为 json 文件中 api 实现
'''
import os
import json
import traceback

# 获取当前工作目录，如果此时在 Crawller 目录下运行，则获取的是 Crawller 目录路径，而不是 DataSaver
current_dir = os.getcwd()
os.chdir(current_dir)
data_dir = current_dir + os.path.sep + 'result'
os.path.exists(data_dir) or os.mkdir(data_dir)

# json.dumps(dict, indent)：将Python对象转换成json字符串
# json.dump(dict, file_pointer)：将Python对象写入json文件

# 目前只有一条指数数据的请求要保存，后续请求多的时候看是否改成异步的
def save_to_json(data, filename, mode):
    '''
    :param data: 要存的数据
    :param filename: 保存数据的文件名
    :param mode: 文件打开模式
    :return: None
    '''
    try:
        data_file = os.path.join(data_dir, filename)
        with open(data_file, mode=mode, encoding='utf8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)  # ensure_ascii=False 保证存为 utf-8 从而中文不会乱码
        print(f"{filename} save_to_json success!, type-{type(data)}")
    except Exception as e:
        print(f"some error occured in JsonSaveApi.save_to_json when save {filename}, type-{type(data)}")
        print(traceback.format_exc())
