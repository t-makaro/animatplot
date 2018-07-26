import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import animatplot as aplt


def psi(x, t):
    return (2**-.5*np.exp(t*1j)*np.sin(np.pi*x)
            + .5*np.exp(t*4j)*np.sin(2*np.pi*x)
            + .5*np.exp(t*9j)*np.sin(3*np.pi*x))


x = np.linspace(0, 1, 20)
t = np.linspace(0, 10, 100)

X, T = np.meshgrid(x, t)
Y1 = psi(X, T).real
Y2 = psi(X, T).imag

timeline = aplt.Timeline(t, 's', 24)

ax = plt.axes(xlim=[0, 1], ylim=[-2, 2])
block1 = aplt.blocks.Line(X, Y1, ax)
block2 = aplt.blocks.Line(X, Y2, ax)

anim = aplt.Animation([block1, block2], timeline)

# Your standard matplotlib stuff
plt.title(r'Particle in a Box: $|\Psi\rangle = \frac{1}{\sqrt{2}}'
          r'|E_1\rangle + \frac{1}{2}|E_2\rangle + \frac{1}{2}|E_3\rangle$',
          y=1.03)
plt.xlabel('position')
plt.ylabel(r'$\Psi$')
plt.legend(['Real', 'Imaginary'])

anim.toggle()
anim.timeline_slider()

# anim.save('test.gif', writer=PillowWriter(fps=24))

plt.show()
