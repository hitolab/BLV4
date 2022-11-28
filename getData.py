import matplotlib.pyplot as plt
import numpy as np
import glob
import re
import os

# 読み込むファイル指定
# filePath = '/Applications/Python/ItoLab/BLV4/results/2/*.txt'



def getData(path):
    count = []
    time = []
    # txtファイルの中身を取得
    file = glob.glob(path)
    print(file)
    f = open(file[-1], 'r')
    data = f.read()
    print(data)
    f.close

    # 時間と数値に分解
    D = data.split()
    j = 0
    for i in D:
        if j % 2 == 0:
            count.append(int(i[14:16]))
        else:
            time.append(int(i))
        j = j + 1

    return count