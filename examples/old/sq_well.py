import matplotlib.pyplot as plt
from animatplot.animate import Animate
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

# Animate will take a single callable or an iterable of callables
ani = Animate((real_part, imag_part), [0, 1], [-2, 2], [0, 10],
              fps=60, res=1000, pre_calc=True)

x = np.linspace(0, 1, 20)
y = 2*x - 1
plt.plot(x, y)

# Your standard matplotlib stuff
plt.title(r'Particle in a Box: $|\Psi\rangle = \frac{1}{\sqrt{2}}'
          r'|E_1\rangle + \frac{1}{2}|E_2\rangle + \frac{1}{2}|E_3\rangle$',
          y=1.03)
plt.xlabel('position')
plt.ylabel(r'$\Psi$')
plt.legend(['Real', 'Imaginary'])

# Add the time slider and play/pause button
ani.toggle()
ani.timeline()

plt.show()

# from matplotlib.animation import PillowWriter
# ani.anim.save('test.gif', writer=PillowWriter(fps=24))
