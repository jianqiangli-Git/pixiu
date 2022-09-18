'''
将数据存为 csv 的 api
'''
import os
import pandas as pd
from Crawller.ConstInfo import VOL_NAME

# 获取当前工作目录，如果此时在 Crawller 目录下运行，则获取的是 Crawller 目录路径，而不是 DataSaver
current_dir = os.getcwd()
os.chdir(current_dir)
data_dir = current_dir + os.path.sep + 'result'
os.path.exists(data_dir) or os.mkdir(data_dir)

def save_to_csv(data, filename, mode):
    try:
        labels = [VOL_NAME[label] for label in VOL_NAME.keys()]
        labels.append("行业标签")
        df1 = pd.DataFrame(data=data, columns=labels)
        df1.to_csv(filename, index=False, mode=mode, encoding='utf_8_sig')
        print(f'{filename} save_to_csv success!')
    except Exception as e:
        print('some error occurred in CSVSaver.save_to_csv')
        print(e)
