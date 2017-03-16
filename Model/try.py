# -*- coding: UTF-8 -*-
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()

# 360度分のデータを作成
ims = []
for i in range(360):
    rad = math.radians(i)
    im = plt.scatter(math.cos(rad), math.sin(rad))
    ims.append([im])

# アニメーション作成
ani = animation.ArtistAnimation(fig, ims, interval=1, repeat_delay=1000)

# 表示
plt.show()