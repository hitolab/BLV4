import threading
import datetime
import os

def measure(filepath):
    #ここに定期実行の内容を書く
    dt_now = datetime.datetime.now()
    val = 100
    f = open(filepath, 'a')
    f.write(dt_now.strftime('%Y-%m-%d-%H-%M-%S ')+str(val)+"\n")
    f.close()
    print("現在のスレッドの数: " + str(threading.activeCount()))
    print("[%s] helohelo!!" % threading.currentThread().getName())
    t=threading.Timer(1,measure(filepath))
    t.start()

if __name__=='__main__':
    filepath = "./result.txt"
    t=threading.Thread(target=measure(filepath))
    t.start()