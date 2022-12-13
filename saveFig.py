# 　一つのグラフを画像として保存するプログラム


import matplotlib.pyplot as plt
import datetime
import numpy as np


figDataPath = "/Users/sunao/python_coding/BLV4/results/1/0035_1.txt"


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
    # 計測開始時刻を引いた値を時間として返す
    timeList = [(e-epochlist[0])/3600 for e in epochlist]
    return timeList, countlist


def _getData(path):
    with open(path) as f:
        text = f.read().splitlines()
        time, data = splitData(text)
    return time, data


def makeFig():
    # データの取得
    time1, data1 = _getData(figDataPath)

    # 横軸表示日数
    # 少数点以下切り上げ。最低でも3以上になるように
    display_days = [int(max(np.ceil(max(time1)/24), 3))]

    fig = plt.figure(figsize=(2.0*5, 5))
    ax1 = fig.add_subplot(1, 1, 1)

    for n, ax in enumerate([ax1]):
        ax.tick_params(length=0)
        print(display_days[n])
        print(24*display_days[n])
        ax.set_xlim(0, 24*display_days[n])
        ax.set_ylim(0, 2000)
        # x軸のメモリ、0から24*dis_daysまで、24間隔で配置（numpyを使う利点）
        ax.set_xticks(np.arange(0, 24*(display_days[n]+1), 24))
        # 24毎に点線を引く
        for i in range(1, display_days[n]):
            ax.axvline(x=24*i, linestyle='--', color='black', linewidth=.5)

    ax1.scatter(time1, data1, color="turquoise", s=6, alpha=0.6)
    
    plt.show()


if __name__ == '__main__':
    makeFig()
