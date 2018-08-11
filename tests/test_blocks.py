from matplotlib.testing import setup
setup()
import numpy as np
import matplotlib.pyplot as plt
import animatplot as amp
from animatplot.testing import animation_compare


@animation_compare(baseline_images='Blocks/Line', nframes=5)
def test_Line():
    x = np.linspace(0, 2*np.pi, 20)
    t = np.linspace(0, 2*np.pi, 5)

    X, T = np.meshgrid(x, t)
    Y = np.sin(X+T)
    block = amp.blocks.Line(X, Y)
    return amp.Animation([block])


@animation_compare(baseline_images='Blocks/Pcolormesh', nframes=3)
def test_Pcolormesh():
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    t = np.linspace(0, 2*np.pi, 3)

    X, Y, T = np.meshgrid(x, x, t)
    Z = np.sin(X**2+Y**2-T)

    block = amp.blocks.Pcolormesh(X[:, :, 0], Y[:, :, 0], Z, t_axis=2)
    return amp.Animation([block])


@animation_compare(baseline_images='Blocks/Imshow', nframes=3)
def test_Imshow():
    x = np.linspace(0, 1, 10)
    X, Y = np.meshgrid(x, x)

    U = []
    for i in range(3):
        U.append(X**2+Y**2+i)

    block = amp.blocks.Imshow(U)
    return amp.Animation([block])


@animation_compare(baseline_images='Blocks/Quiver', nframes=4)
def test_Quiver():
    x = np.linspace(0, 1, 10)
    X, Y = np.meshgrid(x, x)

    U, V = [], []
    for i in range(4):
        U.append(X**2+Y**2+i)
        V.append(X**2+Y**2+i)

    block = amp.blocks.Quiver(X, Y, U, V)
    return amp.Animation([block])


@animation_compare(baseline_images='Blocks/Nuke', nframes=3)
def test_Nuke():
    ax = plt.gca()
    sizes = []

    def animate(i):
        sizes.append(i+1)
        ax.pie(sizes)
    block = amp.blocks.Nuke(animate, ax, 3)
    return amp.Animation([block])
