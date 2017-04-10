import matplotlib.pyplot as plt
from animatplot.animate import AnimateParametric
from numpy import sin, cos, exp, pi


def func0(t):
    return sin(t), cos(t)


def func1(t):
    return t/pi-1, (t/pi/2**.5)**2-1

ani = AnimateParametric(
    (func0, func1), [-1, 1], [-1, 1], [0, 2*pi], fps=60, pre_calc=False)

ani.toggle()
ani.timeline()

plt.show()
