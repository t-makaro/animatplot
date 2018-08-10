import matplotlib
matplotlib.use('agg')
import numpy as np
import animatplot as amp
from animatplot.testing.comparison import compare_animation, BunchOFiles


def test_Line():
    x = np.linspace(0, 2*np.pi, 20)
    t = np.linspace(0, 2*np.pi, 5)

    X, T = np.meshgrid(x, t)
    Y = np.sin(X+T)
    block = amp.blocks.Line(X, Y)
    anim = amp.Animation([block])

    compare_animation(anim, 'Line.png', 5, 1e-3)
