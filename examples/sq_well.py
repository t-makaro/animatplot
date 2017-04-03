import matplotlib.pyplot as plt
from animatplot.animate import Animate
from numpy import sin, exp, pi


def psi(x, t):
    return (2**-.5*exp(t*1j)*sin(pi*x)
            + .5*exp(t*4j)*sin(2*pi*x)
            + .5*exp(t*9j)*sin(3*pi*x))

def p(x, t):
    return 2*abs(psi(x, t))**2

ani = Animate(p, [0, 1], [0, 4.5], [0, 10], fps=30, res=100, pre_calc=True)

plt.title(r'Particle in a Box: $|\Psi\rangle = \frac{1}{\sqrt{2}}'
          r'|E_1\rangle + \frac{1}{2}|E_2\rangle + \frac{1}{2}|E_3\rangle$',
          y=1.03)
plt.xlabel('position')
plt.ylabel(r'$|\Psi|^2$')

ani.toggle()
ani.timeline()
plt.show()
