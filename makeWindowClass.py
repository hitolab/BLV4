import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np
import glob
import getData as gd
# import numpy as py
import math


class PlotWindow():

    filePath1 = 'BLV4/results/1/*.txt'
    figure_canvas1 = sg.Canvas(key='figure_cv1name',
                              # ! サイズを確保しておく。
                              size=(500 * 2, 800))
    layout = [
    [sg.Button('Plot1'), sg.Cancel(), figure_canvas1],
    ]
    # windowを作成
    window = sg.Window('matplotlib graph', layout, finalize=True, resizable=True)   

    # figureを作成する関数
    def draw_plot(filePath1):
        y = gd.getData(filePath1)[1]
        x = range(0, len(y))

        fig = plt.figure()
        print(fig.get_dpi)
        ax = fig.add_subplot()
        ax.plot(x, y)
        ax.set_xlabel("time")
        ax.set_ylabel("count")
        ax.set_xlim(0, 100)
        # ax.set_ylim(0, 100)

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
    return figure_canvas_agg

# windowに書きこむfigureを作成して受け取り
drawing_fig1 = draw_plot(filePath1)

fig_agg1 = draw_figure(window['figure_cv1'].TKCanvas, drawing_fig1)


while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    elif event == 'Plot1':

        drawing_fig1 = draw_plot(filePath1)
        draw_figure(window['figure_cv1'].TKCanvas, drawing_fig1)
        print(figure_canvas1.get_size())
        # fig_agg2.draw()

window.close()
