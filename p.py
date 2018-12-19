#encoding=utf8

import operator
import math

arr_s = dict()
arr_t = {
    'up': 0,
    'down': 0,
}

with open('./a.txt') as f: 
    for line in f: 
        arr_cols = line.strip().split('\t')
        name = arr_cols[0]
        du = float(arr_cols[2])
        if du > 0: 
            arr_t['up'] += 1
        else: 
            arr_t['down'] += 1

        arr_s[name] = du

print  arr_t

def mycmp(x, y): 
    x = math.fabs(x)
    y = math.fabs(y)

    if x == y : 
        return 0
    if x > y: 
        return 1

    return -1;

arr_sorted = sorted(arr_s.items(), 
    cmp=lambda x,y : mycmp(x, y),
    key=operator.itemgetter(1),  reverse=True)

# arr_sorted = sorted(arr_s, key=lambda dict_key: math.fabs(arr_s[dict_key]), reverse=True)

# print arr_sorted
for item in arr_sorted: 
    print '%s\t%s' % (item[0], item[1])

