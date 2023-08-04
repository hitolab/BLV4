"""
Matplotlibのグラフをsg.Imagenに埋め込む

"""
import io
import numpy as np
import matplotlib.pyplot as plt

import PySimpleGUI as sg

def make_data_fig(make=True):
    fig = plt.figure()

    if make:
        # x = np.linspace(0, 2*np.pi, 500)
        x = np.arange(0, 2*np.pi, 0.05*np.pi)
        ax = fig.add_subplot(111)
        ax.plot(x, np.sin(x))
        return fig

    else:
        return fig

def draw_plot_image(fig):
    item = io.BytesIO()
    plt.savefig(item, format='png')
    plt.clf()
    # plt.close('all')
    return item.getvalue()

sg.theme('Light Blue 2')

layout = [[sg.Text('Graph Diasplay')],
          [sg.Button('Display',key='-display-'), sg.Button('clear',key='-clear-'), sg.Cancel()],
          [sg.Image(filename='', key='-image-')]
          ]

window = sg.Window('Plot', layout, location=(100, 100), finalize=True)

while True:
    event, values = window.read()

    if event in (None, 'Cancel'):
        break

    elif event == '-display-':
        fig_ = make_data_fig()
        fig_bytes = draw_plot_image(fig_)
        window['-image-'].update(data=fig_bytes)

    elif event == '-clear-':
        fig_ = make_data_fig(False)
        fig_bytes = draw_plot_image(fig_)
        window['-image-'].update(data=fig_bytes)

window.close()
