import matplotlib.pyplot as plt
import numpy as np

# 乱数を25個ずつ生成
x = np.random.randn(80)
y = np.random.randn(80)

fig = plt.figure(figsize=(6, 4), dpi=72,
                 facecolor='skyblue', linewidth=10, edgecolor='green')

# add_subplot(a,b,c)は、グラフの置き場所をa(縦)*b(横)用意して、左上から右の順番でc番目のところに置く
# 決められた形に整形する
ax1 = fig.add_subplot(4, 1, 1, fc='green', title='ax1')
ax2 = fig.add_subplot(3, 2, 3, fc='red', title='ax2')
ax3 = fig.add_subplot(5, 5, 18, fc='blue', title='ax3')
ax4 = fig.add_subplot(3, 2, 6, fc='black', title='ax4')

# plt.subplots(a,b)は、一気にfigとaxを作成する。a*b個の場所を作る。まとめてaxesに収納される
fig2, ax = plt.subplots(1, 1)

# 散布図の作成。alpha:透明度、s:プロットのサイズ
ax.scatter(x, y, alpha=0.6, s=5)

plt.show()
