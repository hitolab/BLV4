import threading
import datetime
import os
import random
import serial
import time

#送受信コマンドに関してはここを見るべき
#https://github.com/hito1979/BLV/blob/master/src/rs232c/CommunicatorPhotomul.java

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
        print("フォトマル{}:".format(self.no)+dt_now.strftime('%Y-%m-%d-%H-%M-%S ')+"計測した")
        t=threading.Timer(Photomal.measuring_cycle, self.measure)
        t.start()

    def __getVal(self): #計測データを得る
        self.val = random.randint(0,100)
        #接続後こちらを試す
        #self.val = self.measureOnce()


    def start(self): #計測開始
        t=threading.Thread(target=self.measure)
        t.start()

    def __command(char, n=""):
        if n == "":
             ret = (char+"\r").encode('utf-8')
        else:
            ret = char.encode('utf-8') + n.to_bytes(2, byteorder="big")+"\r".encode('utf-8')
        return ret

    def __sendCommand(self, char, n=""):
        if n == "":
            self.ser.write(self.__command(char))
        else:
            self.ser.write(self.__command(char, n))

    def __readMessage(self):
        line = self.ser.readline()
        line = line.strip().decode('UTF-8')
        print(line)
        return line

    def __sendAndListen(self, mes):
        ans = ""
        self.__sendCommand(mes)
        time.sleep(3000)
        ans = self.__readMessage()
        return ans

    def checkConnection(self):
        ans = False
        text = self.__sendAndListen("D").substring(0, 2)
        print("checkPort:")
        if text == "VA":
            print("Port Open!")
        else:
            print("Port was not opened")
            ans = True
        return ans

    def __initialize_communication(self):
        if self.no == 1:
            comport = "COM3"
        elif self.no == 2:
            comport = "COM4"
        elif self.no == 3:
            comport = "COM5"
        elif self.no == 4:
            comport = "COM6"

        self.ser = serial.Serial(comport, baudrate=9600, parity=serial.PARITY_NONE)
        isConnected = self.__checkConnection()

        if isConnected == True:
            self.__sendCommand("D")
            self.__sendCommand("V",Photomal.PMT_VOLTAGE)
            self.__sendcommand("P",Photomal.PMT_integraltime)
            self.__sendcommand("R",Photomal.PMT_measureTimes)

    def __readCount(self):
        b0 = self.ser.read().strip().decode('UTF-8')
        b1 = self.ser.read().strip().decode('UTF-8')
        b2 = self.ser.read().strip().decode('UTF-8')
        b3 = self.ser.read().strip().decode('UTF-8')
        print(b0)
        print(b1)
        print(b2)
        print(b3)
        print("これを数字に直す必要あり、4ビット単位？")
        #int b0=(buf[0] & 0xff)*256*256*256;
		#int b1 =(buf[1] & 0xff)*256*256;
		#int b2 = (buf[2] & 0xff)*256;
		#int b3 = (buf[3] & 0xff);
		#System.out.println(b3);
		#ans = b0+b1+b2+b3;

    def measureOnce(self):
        self.__sendCommand("S")
        time.sleep(1)
        ans = self.__readCount()
        return ans


if __name__=='__main__':
    pm1 = Photomal(1) #フォトマル1を選択;
    pm2 = Photomal(2) #フォトマル2を選択
    pm1.start()
    pm2.start()

    #接続後これを試す
    pm1.__initialize_communication()
    pm1.measureOnce()
