import matplotlib.pyplot as plt
from animatplot.animate3 import AnimateImage as Animate
from numpy import sin, cos, pi


def f(x, y, t):
    return sin(x+2*t) + cos(y+2*t)

ani = Animate(f, [0, 2*pi], [0, 2*pi], [0, 2*pi], fps=30, pre_calc=False)

plt.colorbar()

ani.toggle()
ani.timeline()

plt.show()