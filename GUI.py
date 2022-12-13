import PySimpleGUI as sg
import io
import numpy as np
import matplotlib.pyplot as plt
import makeFig as mf
import os

# macかwinでのパス等切り替え
if os.name == 'nt':
    data = "results/1/0035_1.txt"
    saveFile = "results/images"  
elif os.name == 'posix':
    data = "results/1/0035_1.txt"
    saveFile = "results/images"


def make_data_fig(make=True):
    # 表示させるグラフを作る
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
    # よくわからないが、こうするとグラフを表示させることができるらしい
    # [仮説]メモリに保存してから読み込んでいる？
    item = io.BytesIO()
    plt.savefig(item, format='png')
    plt.clf()
    # plt.close('all')
    return item.getvalue()


def makeSaveWindow():
    save_layout = [
        [sg.Text("ファイル名を入力してください|"), sg.InputText(key='-file_name-')],
        [sg.Text("保存先を選択してください|"), 
        sg.InputText(
            default_text=saveFile,
            key="-saveFile-"), 
            sg.FileBrowse(key="-saveFile-")
        ],
        [sg.Button("save",key="-save-"), sg.Button("back", key="-back-")]
    ]
    return sg.Window("preview", save_layout, finalize=True)

def makeSavedWindow():
    saved_layout = [
        [sg.Text("保存しました")],
        [sg.Button("戻る", key="-back-")]
    ]
    return sg.Window("preview", saved_layout, finalize=True)


# FileBrowseとInputTextは隣に置くだけで連携される
home_layout = [
    [sg.Text("ファイル選択"), sg.InputText(
        default_text=data,
        key="file1"), sg.FileBrowse(key="file1")
     ],
    [sg.Text("ファイルを選択してください", visible=False, key='-error_message-')],
    [sg.Button("preview", key="-preview-"),
     sg.Button("save", visible=False, key="-to_save-"), sg.Button("quit")],
    [sg.Image(filename='', key='-image-')]

]


if __name__=='__main__':
    window = sg.Window("ファイル選択", home_layout, location=(30, 30))
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "quit":
            break

        elif event == '-preview-':
            print("preview作成")
            if (values['file1']):
                # 選択したファイルの情報はvalues["file1"]にある
                data = values['file1']
                fig_ = mf.makeFig(data)
                fig_bytes = draw_plot_image(fig_)
                window['-image-'].update(data=fig_bytes)
                window['-to_save-'].update(visible=True)
                window['-error_message-'].update(visible=False)
            else:
                window['-error_message-'].update(visible=True)

        elif event == "-to_save-":
            print("保存開始")
            save_window = makeSaveWindow()
            event, values = save_window.read()

            if event == '-back-':
                save_window.close()

            elif event == '-save-':
                print("保存")
                fig=mf.makeFig(data)
                saveFile = values['-saveFile-']
                plt.savefig(fname = saveFile+"/"+values['-file_name-'])
                save_window.close()
                
                saved_window = makeSavedWindow()
                event, values = saved_window.read()
                if event == '-back-':
                    saved_window.close()


    window.close()
