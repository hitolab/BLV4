
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
import datetime

cycle = 1 #グラフ更新間隔(秒) (ほんとうは10秒くらいにしたほうが良い)

def splitData(text):
    epochlist = []
    countlist = []
    for line in text:
        timeText, countText = line.split()
        count = int(countText)
        year, month, day, hour, minute, sec = timeText.split('-')
        epoch = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec)).timestamp()
        epochlist.append(epoch)
        countlist.append(count)
    timelist = [(e - epochlist[0])/3600 for e in epochlist]
    return timelist, countlist

def _getData():
    with open("./results/1/0020_1.txt") as f:
        text1 = f.read().splitlines()
        time1, data1 = splitData(text1)
    with open("./results/1/0020_1.txt") as f:
        text2 = f.read().splitlines()
        time2, data2 = splitData(text2)
    return time1, data1, time2, data2

while True:
    #データの取得
    time1, data1, time2, data2 = _getData()
    
    #横軸表示日数
    display_days = [int(max(np.ceil(max(time1)/24), 3)),int(max(np.ceil(max(time2)/24), 3))]
 
    #グラフの描画
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    for n, ax in enumerate([ax1,ax2]):
        ax.tick_params(length=0)
        ax.set_xlim(0, 24*display_days[n])
        ax.set_xticks(np.arange(0, 24*(display_days[n]+1), 24))
        for i in range(1,display_days[n]):
            ax.axvline(x=24*i,linestyle='--',color='black',linewidth=.5)
    ax1.scatter(time1,data1,color="turquoise")
    ax2.scatter(time2,data2,color="violet")
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close()
    cv2.imshow('BLV', img)
    #繰り返し分から抜けるためのif文
    key =cv2.waitKey(1000*cycle)
    if key == ord("h"):
        break

cv2.destroyAllWindows()

