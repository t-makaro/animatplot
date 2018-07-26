import matplotlib.pyplot as plt
import animatplot as aplt
from numpy import sin, exp, pi
import numpy as np


def psi(x, t):
    return (2**-.5*exp(t*1j)*sin(pi*x)
            + .5*exp(t*4j)*sin(2*pi*x)
            + .5*exp(t*9j)*sin(3*pi*x))


def real_part(x, t):
    return psi(x, t).real


def imag_part(x, t):
    return psi(x, t).imag

x = np.linspace(0, 1, 20)
t = np.linspace(0, 10, 100)

X, T = np.meshgrid(x, t)
Y = real_part(X, T)

timeline = aplt.Timeline(t)

ax = plt.gca()
fig = plt.gcf()
block = aplt.blocks.Line(X, Y, ax)
anim = aplt.Animation([block], timeline, fig)

plt.show()
