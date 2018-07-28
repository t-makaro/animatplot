import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import animatplot as aplt


x = np.linspace(0, 2*np.pi, 10)
y = np.linspace(0, 2*np.pi, 5)
t = np.linspace(0, 4.9, 50)

timeline = aplt.Timeline(t)

X, Y, T = np.meshgrid(x, y, t)

U = np.cos(X+T)
V = np.sin(Y+T)

ax = plt.axes(xlim=[-1, 7], ylim=[-1, 7])
block1 = aplt.blocks.Quiver(X, Y, U, V, ax)
anim = aplt.Animation([block1], timeline)

anim.toggle()
anim.timeline_slider()

plt.show()
