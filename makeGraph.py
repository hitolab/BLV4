import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np
import getData as gd
# import numpy as py

# figureを作成する関数
def draw_plot(filePath):
    y = gd.getData(filePath)[1]
    x = range(0, len(y))

    fig = plt.figure()
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
    # print("編集前")
    # print(canvas.children)
    # if canvas.children:
    #     for child in canvas.winfo_children():
    #         child.destroy()
    figure.canvas.flush_events()
    print("編集後")
    print(canvas.children)

    # ここで実際にgui上に書きこむ処理をする
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='left', fill='both', expand=1)
    return figure_canvas_agg

def makeFigureCanvas(name):
    #gui上のfigureを描画するcanvasを定義
    figure_canvas = sg.Canvas(key=name,
                              # ! サイズを確保しておく。
                              size=(500 * 2, 600))
    return figure_canvas


# 読み込むファイル指定
filePath1 = 'BLV4/results/1/*.txt'
filePath2 = 'BLV4/results/2/*.txt'
# グラフ用のキャンバス用意
figure_canvas1 = makeFigureCanvas('figure_cv1')
figure_canvas2 = makeFigureCanvas('figure_cv2')

# レイアウトを定義。画面の構成
layout = [
    [sg.Button('Plot1'), sg.Cancel(), figure_canvas1],
    [sg.Button('Plot2'), sg.Cancel(), figure_canvas2]
]

# windowを作成
window = sg.Window('matplotlib graph', layout, finalize=True)

# windowに書きこむfigureを作成して受け取り
drawing_fig1 = draw_plot(filePath1)
drawing_fig2 = draw_plot(filePath2)

fig_agg1 = draw_figure(window['figure_cv1'].TKCanvas, drawing_fig1)
fig_agg2 = draw_figure(window['figure_cv2'].TKCanvas, drawing_fig2)


while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    elif event == 'Plot1':
        drawing_fig1 = draw_plot(filePath1)
        draw_figure(window['figure_cv1'].TKCanvas, drawing_fig1)
        # fig_agg2.draw()

    elif event == 'Plot2':
        drawing_fig2 = draw_plot(filePath2)
        # fig_agg1.draw()
        draw_figure(window['figure_cv2'].TKCanvas, drawing_fig2)


window.close()
