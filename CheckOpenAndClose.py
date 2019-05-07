from pandas_datareader import data
import pandas as pd
import time
import datetime
import xlrd
import xlwt
import requests
import os
import json

def CheckStock(stock):
    try:
        r_data = {
            'Stock': stock,
            'Open': 0,
            'Close': 0,
            'Close/Open': 0,
            'Volume': 0
            }

        url = 'http://hq.sinajs.cn/list=gb_'+stock

        s = requests.session()
        r = s.get(url)

        result = str(r.content,encoding='gb18030')

        if result.find(',') >= 0:
            data = result.split(",")
            r_data['Stock'] = stock
            r_data['Open'] = float(data[5])
            r_data['Close'] = float(data[1])
            r_data['Volume'] = int(data[10])

            if r_data['Open'] >= 5 and r_data['Open'] <= 15:
                result = abs(r_data['Close'] - r_data['Open'])/r_data['Open']
                if result > 0.08 and r_data['Volume'] > 100000:
                    if r_data['Open'] > r_data['Close']:
                        r_data['Close/Open'] = -result
                    else:
                        r_data['Close/Open'] = result

                    return r_data

    except e:
        print(e.message)


def GetStockResult(file):
    arr_s = dict()
    arr_t = { 'up': 0 , 'down': 0}

    with open(file,encoding='utf8') as f:
        for line in f:
            f2 = line.strip("\n\r")

            result = CheckStock(f2)
            if result != None:
                name = result['Stock'] 
                if result['Close/Open'] > 0:
                    arr_t['up'] += 1
                else:
                    arr_t['down'] += 1
                
                arr_s[name] = {'result':result['Close/Open'],'open':result['Open'],'close':result['Close'],'volume':result['Volume']}
                
        f.close()
    
    '''
    print("List Result============================")
    print(arr_t)
    '''

    arr_sorted = sorted(arr_s.items(),key=lambda x:(x!=0,abs(x[1]['result'])),reverse=True)

    '''
    for item in arr_sorted:     
        print(item)
    '''

    return {'Result': arr_t, 'Details': arr_sorted}


def DicSaveToTxt(filename,dic_data):
    path_file_name = "E:\\Result\\" + filename + ".txt"

    if not os.path.exists(path_file_name):
        with open(path_file_name,"w") as f:
            print(f)
    
    with open(path_file_name,"a") as f:
        for l in dic_data:
            r = json.dumps(dic_data[l])
            f.write(l + " : ")
            f.write(r)
            f.write('\n')
    
    f.close()

def ListSaveToTxt(filename,list_data):
    path_file_name = "E:\\Result\\" + filename + ".txt"

    if not os.path.exists(path_file_name):
        with open(path_file_name,"w") as f:
            print(f)
    
    with open(path_file_name,"a") as f:
        for l in list_data:
            f.write(str(l))
            f.write('\n')
    
    f.close()

def main():
    print("Start============================")

    filePath = r'E:\VS\CheckOpenAndClose\CheckOpenAndClose\StockCode.txt'

    fileName = str(datetime.datetime.now()).split(' ')[0]
    fileName = fileName.replace('-','')

    result = GetStockResult(filePath)

    DicSaveToTxt(fileName,result['Result'])
    ListSaveToTxt(fileName,result['Details'])

    print("Done=============================")



if __name__ == '__main__':
    main()