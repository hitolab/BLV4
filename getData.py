import glob

def getData(path):
    count = []
    time = []
    # txtファイルの中身を取得
    file = glob.glob(path)
    f = open(file[-1], 'r')
    data = f.read()
    f.close
    # 時間と数値に分解
    D = data.split()
    j = 0
    for i in D:
        if j % 2 == 0:
            print(i)
            time.append(i[0:10])
        else:
            print(i)
            count.append(int(i))
        j = j + 1

    return count,time