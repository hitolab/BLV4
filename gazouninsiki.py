##Jerryfish Tracker
#1. 実行すると、画面が現れる
#2. クリックで1番目のROI, シフト+クリックで2番目のROI
#3. dを押すと特徴点を抽出, トラッキングスタート
#4. クリックまたはクリック+シフトでグラフに表示されている特徴点を変更可能。
#5. hで終了, rで#1にもどる
​
​
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
​
#webカメラの設定
cap = cv2.VideoCapture(0) #どのwebカメラをつかうかは、ffmpeg -list_devices true -f avfoundation -i dummyでわかる。
#print(cap.get(cv2.CAP_PROP_FOCUS))
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 0.5)
#print(cap.get(cv2.CAP_PROP_FOCUS))
​
#グラフの描画
ind1 = np.ones(500)
ind2 = np.ones(500)
ind1_idx = 0 #1番目のグラフで注目するデフォルトのindex
ind2_idx = 1 #2番目のグラフで注目するデフォルトのindex
newpoint = [[],[]]
​
#クリックで探索範囲指定
x_click1, y_click1, x_click2, y_click2 = -1,-1,-1,-1
​
#探索範囲の幅
length = 100
​
#クリックした場所の取得
def onMouse(event, x_click, y_click, flags, params):
    global ind1_idx, ind2_idx
​
    if event == cv2.EVENT_LBUTTONDOWN and flags & cv2.EVENT_FLAG_SHIFTKEY:
        for i in range(len(newpoint[0])):
            if ((x_click - newpoint[0][i])**2 + (y_click - newpoint[1][i])**2)**0.5 < 30:
                ind2_idx = i
    elif event == cv2.EVENT_LBUTTONDOWN:
        for i in range(len(newpoint[0])):
            if ((x_click - newpoint[0][i])**2 + (y_click - newpoint[1][i])**2)**0.5 < 30:
                ind1_idx = i
​
#クリックして探索範囲決定
def onMouse2(event, x_click, y_click, flags, parame):
    global x_click1, y_click1, x_click2, y_click2
​
    if event == cv2.EVENT_LBUTTONDOWN and flags & cv2.EVENT_FLAG_SHIFTKEY:
        x_click2 = x_click
        y_click2 = y_click
    elif event == cv2.EVENT_LBUTTONDOWN:
        x_click1 = x_click
        y_click1 = y_click
​
def makemask(originalmask):
    #global x_click1, y_click1, x_click2, y_click2
    ans = originalmask
    windowx = originalmask.shape[0]
    windowy = originalmask.shape[1]
​
    if x_click1 >= 0:
        for i in range(y_click1 -length,  y_click1 + length):
            for j in range(x_click1 -length, x_click1 + length):
                modi = i % windowx
                modj = j % windowy
                ans[modi][modj] = 1
    if x_click2 >= 0:
        for i in range(y_click2 -length,  y_click2 +length):
            for j in range(x_click2 -length, x_click2 + length):
                modi = i % windowx
                modj = j % windowy
                ans[modi][modj] = 1    
    return ans
​
def specifyLoop():
    #特徴点決定のための無限ループ
    while True:
        #クリックうけつけ
        cv2.setMouseCallback("camera", onMouse2)
​
        #カメラからの画像取得
        _, frame = cap.read()
    
        #選択範囲の四角描画
        if x_click1>= 0:
            frame = cv2.rectangle(frame, (x_click1 - length, y_click1 - length),(x_click1 + length, y_click1 + length),(64, 224, 208),2)
        if x_click2>= 0:
            frame = cv2.rectangle(frame, (x_click2 - length, y_click2 - length),(x_click2 + length, y_click2 + length),(238, 130, 238),2)
​
        #カメラの画像の出力
        cv2.imshow('camera' , frame)
​
        #繰り返し分から抜けるためのif文
        key =cv2.waitKey(10)
        if key == ord("d"): #特徴点を抽出
            break
​
​
def detectionLoop():
    global ind1,ind2, ind1_idx, ind2_idx, newpoint
​
    # グレースケールにしてコーナ特徴点を抽出
    _, frame = cap.read()
    #prev_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    Blue,Green,Red = cv2.split(frame)
    prev_gray = Red
​
    mask = np.zeros_like(prev_gray)
    mask = makemask(mask)
​
    #特徴点解析
    feature_params = {
        "maxCorners": 10,  # 特徴点の上限数
        "qualityLevel": 0.005,  # 閾値　（高いほど特徴点数は減る)
        "minDistance": 30,  # 特徴点間の距離 (近すぎる点は除外)
        "blockSize": 12  #
    }
    p0 = cv2.goodFeaturesToTrack(prev_gray, mask=mask, **feature_params)
​
    # 特徴点をプロットして可視化
    for p in p0:
        x,y = p.ravel()
        cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 255) , thickness=-1)
​
    # OpticalFlowのパラメータ
    lk_params = {
        "winSize": (15, 15),  # 特徴点の計算に使う周辺領域サイズ
        "maxLevel": 2,  # ピラミッド数 (デフォルト0で、2の場合は1/4の画像まで使われる)
        "criteria": (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)  # 探索アルゴリズムの終了条件
    }
​
    #計測のための無限ループ
    color = np.random.randint(0, 255, (200, 3)) 
    mask = np.zeros_like(frame)
    cnt = 0
    firstloop = True
    flag = True
​
    while flag:
        #カメラからの画像取得
        _, frame = cap.read()  
        #frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        Blue,Green,Red = cv2.split(frame)
        frame_gray = Red
​
        # OpticalFlowの計算
        p1, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, frame_gray, p0, None, **lk_params)
​
        # フレーム前後でトラックが成功した特徴点のみをのこす
        identical_p1 = p1[status==1]
        identical_p0 = p0[status==1]
​
        #新しいデータポイント
        newpoint_x = []
        newpoint_y = []
​
        # 可視化のためのプログラム
        for i, (p1, p0) in enumerate(zip(identical_p1, identical_p0)):
            p1_x, p1_y = p1.ravel()
            p0_x, p0_y = p0.ravel()
            mask = cv2.line(mask, (int(p1_x), int(p1_y)), (int(p0_x), int(p0_y)), color[i].tolist(), 2)
            radius = 5
            col = color[i].tolist()
            if i == ind1_idx:
                radius = 10
                col = [64, 224, 208]
            if i == ind2_idx:
                radius = 10
                col = [238, 130, 238]
​
            frame = cv2.circle(frame, (int(p1_x), int(p1_y)), radius, col, -1)
            newpoint_x = newpoint_x + [int(p1_x)]
            newpoint_y = newpoint_y + [int(p1_y)]
        newpoint = [newpoint_x,newpoint_y]
​
        # 可視化用の線・円を重ねて表示
        image = cv2.add(frame, mask)
​
        #グラフデータ作成
        pointnum = len(newpoint[0])
        if firstloop == False:
            ind1 = np.append(newpoint[1][min(ind1_idx,pointnum-1)], ind1[:-1])
            ind2 = np.append(newpoint[1][min(ind2_idx,pointnum-1)], ind2[:-1])
        else:
            ind1 = ind1*newpoint[1][min(ind1_idx,pointnum-1)]
            ind2 = ind2*newpoint[1][min(ind2_idx,pointnum-1)]
            firstloop = False
​
        #グラフ描画
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1)
        ax2 = fig.add_subplot(2,1,2)
        for ax in [ax1,ax2]:
            ax.tick_params(length=0)
            ax.tick_params(labelbottom=False,labelleft=False)
            ax.set_xlim(0, 500)
            ax.set_xlim(0, 500)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
        ax1.plot(ind1,color="turquoise")
        ax2.plot(ind2,color="violet")
        fig.canvas.draw()
        image_g = np.array(fig.canvas.renderer.buffer_rgba())
        image_g = np.delete(image_g, 3, axis=2)
​
        #リサイズして結合
        width = image.shape[1]
        image_g = cv2.resize(image_g, (width, 400))
        image = cv2.vconcat([image, image_g])
        plt.clf()
        plt.close()
​
        #表示
        cv2.imshow("camera", image)
        cv2.setMouseCallback("camera", onMouse)
​
        # トラックが成功した特徴点のみを引き継ぐ
        prev_gray = frame_gray.copy()
        p0 = identical_p1.reshape(-1, 1, 2)
​
        # たまにmaskをけす
        if cnt > 100:
            cnt = 0
            mask = np.zeros_like(frame)
        else:
            cnt = cnt + 1
​
        #繰り返し分から抜けるためのif文
        key =cv2.waitKey(10)
        if key == ord("r"):
            break
        elif key == ord("h"):
            flag = False 
        
    #hを押された場合は返り値がFalse
    return flag
        
​
def closeWindows():
    #メモリを解放して終了する
    cap.release()
    cv2.destroyAllWindows()
​
#プログラム本体
​
while True:
    specifyLoop()
    loop = detectionLoop()
    if loop == False:
        break
closeWindows()