#encoding=utf8
import operator
import math

arr_s = dict()
arr_t = {    'up': 0,    'down': 0,}

with open(r'.\a.txt',encoding='utf8') as f: 
    for line in f:         
        arr_cols = line.strip().split('####')        
        name = arr_cols[0]        
        du = float(arr_cols[2])        
        if du > 0:             
            arr_t['up'] += 1        
        else:             
            arr_t['down'] += 1        
        
        arr_s[name] = du
        
print(arr_t)


arr_sorted = sorted(arr_s.items(),key=lambda x:(x[1]<0,abs(x[1])),reverse=True)


for item in arr_sorted:     
    print(item)
