import threading
import datetime
import os
import random
import serial
import time

class Photomal:

    measuring_cycle = 60 #60秒間隔で測定(実際は10分くらいで良いと思う);
    PMT_VOLTAGE = 1000 #PMTの電圧
    PMT_integraltime = 100 #積算時間
    PMT_measureTimes = 1 #計測回数

    def __init__(self, no):

        fileno = len(os.listdir(path="./results/{}".format(no)))+1
        self.no = no
        self.filepath = "./results/{}/{:04}_{}.txt".format(self.no,fileno,self.no)
        self.__initialize_communication()

    def measure(self):
        #ここに定期実行の内容を書く
        dt_now = datetime.datetime.now()
        self.__getVal()
        f = open(self.filepath, 'a')
        f.write(dt_now.strftime('%Y-%m-%d-%H-%M-%S ')+str(self.val)+"\n")
        f.close()
        print("PMT{}:".format(self.no)+dt_now.strftime('%Y-%m-%d-%H-%M-%S ')+"measured "+str(self.val))
        #ここまで定期実行
        # t=threading.Timer(Photomal.measuring_cycle, self.measure)
        # t.start()

    def __getVal(self): #計測データを得る
        self.val = self.measureOnce()


    def start(self): #計測開始
        t=threading.Thread(target=self.measure)
        t.start()

    def __command(self,char, n=""):
        if n == "":
             ret = (char+"\r").encode('utf-8')
        elif n >255:
            ret = char.encode('utf-8') + n.to_bytes(2, byteorder="big")+"\r".encode('utf-8')
        else:
            ret = char.encode('utf-8') + n.to_bytes(1, byteorder="big")+"\r".encode('utf-8')
        return ret

    def __sendCommand(self, char, n=""):
        print("SEND PMT{}: {} {}".format(self.no, char, n))
        if n == "":
            self.ser.write(self.__command(char))
        else:
            self.ser.write(self.__command(char, n))

    def __readMessage(self, num):
        receivedMsg =""
        for i in range(num):
            char = self.ser.read()
            char = char.strip().decode('UTF-8')
            receivedMsg = receivedMsg + char
        print("RECEIVE PMT{}: {}".format(self.no, receivedMsg))
        return receivedMsg

    def __sendAndListen(self, mes, n=""):
        self.__sendCommand(mes, n)
        time.sleep(1)
        ans = self.__readMessage(2)
        return ans

    def checkConnection(self):
        ans = False
        text = self.__sendAndListen("D")
        print("checkPort... ", end="")
        if text == "VA":
            print("Port Open!")
            ans = True
        else:
            print("Port was not opened")

        return ans

    def __initialize_communication(self):
        if self.no == 1:
            comport = "COM1"
        elif self.no == 2:
            comport = "COM2"
        elif self.no == 3:
            comport = "COM3"
        elif self.no == 4:
            comport = "COM4"

        self.ser = serial.Serial(comport, baudrate=9600, parity=serial.PARITY_NONE)
        isConnected = self.checkConnection()

        if isConnected == True:
            self.__sendAndListen("V",Photomal.PMT_VOLTAGE)
            self.__sendAndListen("P",Photomal.PMT_integraltime)
            self.__sendAndListen("R",Photomal.PMT_measureTimes)

    def __readCount(self):
        b0 = int.from_bytes(self.ser.read(),'big')*256*256*256
        b1 = int.from_bytes(self.ser.read(),'big')*256*256
        b2 = int.from_bytes(self.ser.read(),'big')*256
        b3 = int.from_bytes(self.ser.read(),'big')

		#System.out.println(b3);
        return b0+b1+b2+b3

    def measureOnce(self):
        self.__sendCommand("S")
        time.sleep(2)
        ans = self.__readCount()
        return ans


if __name__=='__main__':
    pm1 = Photomal(1) #フォトマル1を起動
    #pm2 = Photomal(2) #フォトマル2を起動
    pm1.start() #周期的測定開始
    #pm2.start() #周期的測定開始
