import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import getData as gd
from Photomal import Photomal
import random

x = []
y = []
i = 0
cycleTime = 0.5
# filePath = 'results/1/*.txt'

if __name__ == '__main__':
    # pm1 = Photomal(1)
    # pm1.start()

    while True:
        # pm1.print()

        y.append(int(random.randrange(0, 50)))
        # y.append(gd.getData(filePath)[0])
        x.append(i)

        fig, ax = plt.subplots(1, 1)
        
        ax.plot(x, y)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 60)
        ax.tick_params(length=0)
        ax.tick_params(labelbottom=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # グラフ描画 & t秒後次に進む
        plt.pause(cycleTime)

        # clf():fig,axともに消去する
        # plt.clf()
        # windowを閉じる。figureも消去
        plt.close()

        # ループ回数カウント
        i += 1
