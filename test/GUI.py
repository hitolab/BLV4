import PySimpleGUI as sg

# FileBrowseとInputTextは隣に置くだけで連携される
home_layout = [
    [sg.Text("ファイル"), sg.InputText(), sg.FileBrowse(key="file1")],
    [sg.Button("preview")],
    [sg.Cancel()]
]


def makePreview():
    preview_layout = [
        [sg.Text("ファイル"), sg.InputText(), sg.FileBrowse(key="file1")],
        [sg.Image(
            filename='2022-11-2.png')],
        [sg.Button("save"), sg.Cancel()]
    ]
    return sg.Window("preview", preview_layout, finalize=True)


def makeFinishlog():
    preview_layout = [
        [sg.Text("保存しました")],
        [sg.Cancel()]
    ]
    return sg.Window("preview", preview_layout, finalize=True)


window = sg.Window("ファイル選択", home_layout)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Cancel":
        break

    elif event == "preview":
        window.close()
        window = makePreview()

    elif event == "save":
        window.close()
        window = makeFinishlog()


window.close()
