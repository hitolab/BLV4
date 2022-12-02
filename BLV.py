
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random

cycle = 1 #グラフ更新間隔(秒) (ほんとうは10秒くらいにしたほうが良い)

def _getData():
    with open("./fig/")
    time = np.arange(1, 73, 1)
    data1 = [random.randint(0, 10) for i in range(72)]
    data2 = [random.randint(0, 10) for i in range(72)]
    return time, data1, data2

while True:
    #データの取得
    time, data1, data2 = _getData()
    
    #横軸表示日数
    display_days = int(max(np.ceil(max(time)/24), 5))

    #グラフの描画
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    for ax in [ax1,ax2]:
        ax.tick_params(length=0)
        ax.tick_params(labelbottom=False,labelleft=False)
        ax.set_xlim(0, 24*display_days)
        for i in range(1,display_days):
            ax.axvline(x=24*i,linestyle='--',color='black',linewidth=.5)
    ax1.plot(time,data1,color="turquoise")
    ax2.plot(time,data2,color="violet")
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close()
    cv2.imshow('BLV', img)
    #繰り返し分から抜けるためのif文
    key =cv2.waitKey(1000*cycle)
    if key == ord("h"):
        break

cv2.destroyAllWindows()

