# BioLuminescenceView ver.4
# いまのところは hでソフトウェアが終了します。

import matplotlib.pyplot as plt
import numpy as np
import cv2
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

# 富永くんへ：ファイルの読み込み先が適切になるように記述してください。
# さらにいま２つのふぁいるの読み込み先が同じになっていますが、いずれ別々にするのが良いと思います。
# さらにクリックに応じて、フォトマル1やフォトマル2が計測スタートするようにするといいでしょうね。


def _getData():
    with open(glob.glob("./results/1/*.txt")[-1]) as f:
        text1 = f.read().splitlines()
        time1, data1 = splitData(text1)
    with open(glob.glob("./results/2/*.txt")[-1]) as f:
        text2 = f.read().splitlines()
        time2, data2 = splitData(text2)
    with open(glob.glob("./results/3/*.txt")[-1]) as f:
        text3 = f.read().splitlines()
        time3, data3 = splitData(text3)
    with open(glob.glob("./results/4/*.txt")[-1]) as f:
        text4 = f.read().splitlines()
        time4, data4 = splitData(text4)
    return time1, data1, time2, data2,time3, data3, time4, data4

def BLVrun():
    while True:
        # データの取得
        time1, data1, time2, data2, time3, data3, time4, data4 = _getData()

        # 横軸表示日数
        display_days = [int(max(np.ceil(max(time1)/24), 3)),
                        int(max(np.ceil(max(time2)/24), 3)),
                        int(max(np.ceil(max(time3)/24), 3)),
                        int(max(np.ceil(max(time4)/24), 3))
                        ]

        # グラフの描画
        fig = plt.figure()
        ax1 = fig.add_subplot(4, 1, 1)
        ax2 = fig.add_subplot(4, 1, 2)
        ax3 = fig.add_subplot(4, 1, 3)
        ax4 = fig.add_subplot(4, 1, 4)
        
        for n, ax in enumerate([ax1, ax2, ax3, ax4]):
            ax.tick_params(length=0)
            ax.set_xlim(0, 24*display_days[n])
            ax.set_xticks(np.arange(0, 24*(display_days[n]+1), 24))
            for i in range(1, display_days[n]):
                ax.axvline(x=24*i, linestyle='--', color='black', linewidth=.5)
        ax1.scatter(time1, data1, color="turquoise", s=6, alpha=0.6)
        ax2.scatter(time2, data2, color="violet", s=6, alpha=0.6)
        ax3.scatter(time3, data3, color="turquoise", s=6, alpha=0.6)
        ax4.scatter(time4, data4, color="violet", s=6, alpha=0.6)
        fig.canvas.draw()
        img = np.array(fig.canvas.renderer.buffer_rgba())
        plt.close()
        cv2.imshow('BLV', img)
        # 繰り返し分から抜けるためのif文
        key = cv2.waitKey(100*cycle)
        if key == ord("h"):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    pm1 = Photomal.Photomal(1)  # フォトマル1を起動
    pm1.start()  # 周期的測定開始
    print("pm1start")
    time.sleep(3)
    pm2 = Photomal.Photomal(2)  # フォトマル1を起動
    pm2.start()  # 周期的測定開始
    print("pm2start")
    BLVrun()
