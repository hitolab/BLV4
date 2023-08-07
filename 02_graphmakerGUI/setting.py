import PySimpleGUI as sg

def main():
    layout = [
        [sg.Text('整数を入力してください：')],
        [sg.InputText(key='-INPUT-', justification='center')],
        [sg.Button('OK'), sg.Button('キャンセル')]
    ]

    window = sg.Window('数字入力', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'キャンセル':
            break

        input_text = values['-INPUT-']

        try:
            # 入力が整数かどうかチェック
            int_input = int(input_text)
            # ウィンドウを閉じる
            window.close()
            break
        except ValueError:
            # 入力が整数でない場合、エラーメッセージを表示
            sg.popup_error('整数を入力してください。', title='エラー')

    window.close()

    # もし入力が成功した場合、入力された整数を返す
    if 'int_input' in locals():
        return int_input
    else:
        return None

if __name__ == '__main__':
    result = main()
    if result is not None:
        print('入力された整数：', result)
