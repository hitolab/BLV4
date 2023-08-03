import turbidsystem.Photomal as Photomal
import matplotlib.pyplot as plt
import numpy as np
import time

plt.ion()
fig= plt.figure(figsize=(12,6))
ax = fig.add_subplot(2,1,1)
ax.tick_params(length=0)
ax.tick_params(labelbottom=False, labelleft=False)
x = np.arange(0, 2*np.pi, 0.1)
y = np.sin(x)
line1, = ax.plot(x, y)
plt.draw()
y = np.cos(x)
line1.set_ydata(y)
plt.pause(3)


#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
#ax.spines['bottom'].set_visible(True)
#ax.spines['left'].set_visible(True)



#pm1 = Photomal(1) #フォトマル1を起動
#pm2 = Photomal(2) #フォトマル2を起動
#pm1.start() #周期的測定開始
#pm2.start() #周期的測定開始