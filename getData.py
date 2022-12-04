import glob

# def getData(path):
#     count = []
#     time = []
#     # txtファイルの中身を取得
#     file = glob.glob(path)
#     f = open(file[-1], 'r')
#     data = f.read()
#     f.close
#     # 時間と数値に分解
#     D = data.split()
#     j = 0
#     for i in D:
#         if j % 2 == 0:
#             print(i)
#             time.append(i[0:10])
#         else:
#             print(i)
#             count.append(int(i))
#         j = j + 1

#     return count,time

import datetime
import os
from pathlib import Path


# startからpathへの相対パスを取得
path = "/Applications/Python/ItoLab/BLV4/results/1/0020_1.txt"
start = "/Applications/Python/ItoLab/BLV4/getData.py"

# print(os.path.relpath(path, start))

# 出力結果：../results/1/0020_1.txt

# カレントディレクトリを表示させて、ファイルの場所があっているかチェック
# 今回は、../でBLV4の外まで行っているのにBLV4を書いてなかった
print(os.getcwd())


def splitData(text):
    epochlist = []
    countlist = []
    for line in text:
        timeText, countText = line.split()
        count = int(countText)
        year, month, day, hour, minute, sec = timeText.split('-')
        epoch = datetime.datetime(int(year), int(month), int(
            day), int(hour), int(minute), int(sec)).timestamp()
        epochlist.append(epoch)
        countlist.append(count)
    timelist = [(e - epochlist[0])/3600 for e in epochlist]
    return timelist, countlist


filePath1 = 'BLV4/results/1/*.txt'


def _getData():
    with open(glob.glob("./results/1/*.txt")[-1]) as f:
        text1 = f.read().splitlines()
        time1, data1 = splitData(text1)
    with open(glob.glob("./results/2/*.txt")[-1]) as f:
        text2 = f.read().splitlines()
        time2, data2 = splitData(text2)
    print(time1, data1, time2, data2)

if __name__ == '__main__':
    _getData()
