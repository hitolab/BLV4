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

# オリジナルテーマの作成
sg.LOOK_AND_FEEL_TABLE['MyNewTheme'] = {
    'BACKGROUND': 'LightBlue1',
    'TEXT': 'azure4',
    'INPUT': 'white smoke',
    'SCROLL': '#E3E3E3',
    'TEXT_INPUT': 'azure4',
    'BUTTON': ('sky blue', 'white smoke'),
    'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
    'BORDER': 0,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}

mouseoverColors = ('white smoke', 'skyblue')
quitButtonMouseoverColor = ('white smoke', 'PaleVioletRed1')
quitButtonColor = ('white smoke', 'pink1')


def draw_plot_image(fig):
    # よくわからないが、こうするとグラフを表示させることができるらしい
    # [仮説]メモリに保存してから読み込んでいる？
    item = io.BytesIO()
    plt.savefig(item, format='png')
    plt.clf()
    # plt.close('all')
    return item.getvalue()


def makeHomeWindow():
    # FileBrowseとInputTextは隣に置くだけで連携される
    home_layout = [
        [sg.Text("ファイル選択"), sg.InputText(
            default_text=data,
            key="file1"), sg.FileBrowse(key="file1")
         ],
        [sg.Text("ファイルを選択してください", visible=False, key='-error_message-')],
        [sg.Button("preview", key="-preview-", bind_return_key=True, mouseover_colors=mouseoverColors),
         sg.Button("save", disabled=True, key="-to_save-",
                   mouseover_colors=mouseoverColors),
         sg.Button("quit", key="-quit-", button_color=quitButtonColor, mouseover_colors=quitButtonMouseoverColor)],
        [sg.Image(filename='', key='-image-')]
    ]
    return sg.Window("ファイル選択", home_layout, location=(30, 30), return_keyboard_events=True, no_titlebar=True)


def makeSaveWindow():
    save_layout = [
        [sg.Text("ファイル名を入力してください|"), sg.InputText(key='-file_name-')],
        [sg.Text("保存先を選択してください|"),
         sg.InputText(
            default_text=saveFile,
            key="-saveFile-"),
            sg.FileBrowse(key="-saveFile-")
         ],
        [sg.Button("save", key="-save-", bind_return_key=True, mouseover_colors=mouseoverColors),
         sg.Button("back", key="-back-", button_color=quitButtonColor, mouseover_colors=quitButtonMouseoverColor)]
    ]
    return sg.Window("preview", save_layout, finalize=True, element_justification='right', size=(500, 80))


def makeSavedWindow():
    saved_layout = [
        [sg.Text("保存しました")],
        [sg.Button("戻る", key="-back-", button_color=quitButtonColor,
                   mouseover_colors=quitButtonMouseoverColor, bind_return_key=True)]
    ]
    return sg.Window("preview", saved_layout, finalize=True, size=(500, 80))


if __name__ == '__main__':
    # テーマの適用
    sg.theme('MyNewTheme')
    window = makeHomeWindow()
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "-quit-":
            break

        elif event == '-preview-':
            print("preview作成")
            if (values['file1']):
                # 選択したファイルの情報はvalues["file1"]にある
                data = values['file1']
                fig_ = mf.makeFig(data)
                fig_bytes = draw_plot_image(fig_)
                window['-image-'].update(data=fig_bytes)
                window['-to_save-'].update(disabled=False)
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
                plt.savefig(fname=saveFile+"/"+values['-file_name-'])
                save_window.close()

                saved_window = makeSavedWindow()
                event, values = saved_window.read()
                if event == '-back-':
                    saved_window.close()

    window.close()
