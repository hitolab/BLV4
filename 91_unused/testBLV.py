# グラフを四つ表示させるための練習
# 定義等をループ使ってきれいに書いたが動作せず

import matplotlib.pyplot as plt
import numpy as np
import datetime
import turbidsystem.Photomal as Photomal
import glob
import time

cycle = 10  # グラフ更新間隔(秒) (ほんとうは10秒くらいにしたほうが良い)


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


def _getData():
    time = []
    data = []
    for i in range(4):
        # sortedで名前順にする→最新=[-1]を読み込む
        files = sorted(glob.glob("./results/{}/*.txt".format(i+1)))
        print(files)
        with open(files[-1]) as f:
            text = f.read().splitlines()
            time.append(splitData(text)[0])
            data.append(splitData(text)[1])
    return time, data


def BLVrun():
    # データの取得
    time, data = _getData()
    
    # 横軸表示日数
    display_days = []
    for i in range(len(time)):
        display_days.append(int(max(np.ceil(max(time[i])/24), 3)))

    # グラフの描画
    fig = plt.figure()
    ax1 = fig.add_subplot(4, 1, 1)
    ax2 = fig.add_subplot(4, 1, 2)
    ax3 = fig.add_subplot(4, 1, 3)
    ax4 = fig.add_subplot(4, 1, 4)
    axes = [ax1, ax2, ax3, ax4]

    for n, ax in enumerate(axes):
        ax.tick_params(length=0)
        ax.set_xlim(0, 24*display_days[n])
        ax.set_xticks(np.arange(0, 24*(display_days[n]+1), 24))
        for i in range(1, display_days[n]):
            ax.axvline(x=24*i, linestyle='--', color='black', linewidth=.5)

    for n, ax in enumerate(axes):
        ax.scatter(time[n], data[n], color="turquoise", s=6, alpha=0.6)

    plt.show()


if __name__ == '__main__':
    print("main")
    # _getData()
    BLVrun()
