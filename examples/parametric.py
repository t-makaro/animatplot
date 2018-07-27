import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import animatplot as aplt


def psi(t):
    x = t
    y = np.sin(t)
    return x, y


t = np.linspace(0, 2*np.pi, 100)
x, y = psi(t)
X, Y = aplt.util.parametric_line(x, y)

timeline = aplt.Timeline(t, 's', 24)

ax = plt.axes(xlim=[0, 7], ylim=[-1.1, 1.1])
block1 = aplt.blocks.Line(X, Y, ax)
# or equivalently
# block1 = aplt.blocks.ParametricLine(x, y, ax)

anim = aplt.Animation([block1], timeline)

# Your standard matplotlib stuff
plt.title('Parametric Line')
plt.xlabel('x')
plt.ylabel(r'y')

anim.toggle()
anim.timeline_slider()

# anim.save('parametric.gif', writer=PillowWriter(fps=24))

plt.show()
