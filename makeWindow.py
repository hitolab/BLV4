import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import getData as gd
import math
import time
import threading

from Photomal import Photomal

# 場合にかかわらず最初に設定するもの
# 読み込むファイル
# Macなら上、Windowsなら下の書き方
# filePath1 = 'BLV4/results/1/*.txt'
filePath1 = "C:\\Users\\今井圭子\\Documents\\BLV4\\results\\1\\*.txt"
# グラフ用のキャンバス
figure_canvas1 = sg.Canvas(key='figure_cv1', size=(500 * 2, 800))
# 画面の構成
layout = [
    [sg.Button('ReLoad'), sg.Cancel(), figure_canvas1],
]
# windowを作成
window = sg.Window('Graph', layout, finalize=True, resizable=True)

# 更新するたびに新しく読み込む必要があるもの

#テスト用コメント
# figureを作成する関数
def make_figure(filePath):
    y = gd.getData(filePath)
    x = range(0, len(y))

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(x, y)
    ax.set_xlabel("time")
    ax.set_ylabel("count")
    ax.set_xlim(0, 20)

    return fig

# グラフをgui window上のcanvasに描画する関数


def draw_figure(canvas, figure):
    # # 更新処理がされた時に一旦グラフを消去する
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure.canvas.flush_events()
    # ここで実際にgui上に書きこむ処理をする
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='left', fill='both', expand=1)

# 更新処理：図の再プロット＋キャンバスに再配置
def update():
    drawing_fig1 = make_figure(filePath1)
    draw_figure(window['figure_cv1'].TKCanvas, drawing_fig1)


update()

# 1分毎に実行する処理


# def show_window():
#     update()
#     event, values = window.read(timeout=100,timeout_key='-timeout-')

#     if event in (sg.WIN_CLOSED, 'Cancel'):
#         window.close
#         time.sleep(3)
#         print("再起動")
#         show_window()
#     elif event == "ReLoad":
#         update()
#         # 縮小するけど更新
#         show_window()
#     elif event in '-timeout-':
#         print("timeout")

# show_window()


if __name__ == '__main__':
#     t = threading.Thread(target=show_window)
#     t.start()

    pm1 = Photomal(1)
    pm1.start()
    thread = pm1.measure

    while True:
        event, values = window.read(timeout=3000,timeout_key='-timeout-')

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

        elif event == 'ReLoad':
            update()
        elif event in '-timeout-':
            print("timeout")
            threading.Thread(target=pm1.measure, daemon=True).start()
            time.sleep(2)
            update()
            time.sleep(2)

