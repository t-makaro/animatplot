import matplotlib
matplotlib.use('agg')
import numpy as np
import animatplot as amp
from animatplot.testing import animation_compare


@animation_compare(baseline_images='Animation/controls', nframes=5)
def test_controls():
    x = np.linspace(0, 1, 5)
    y = np.sin(np.pi*x)

    block = amp.blocks.ParametricLine(x, y)
    block.ax.set_xlim([0, 1])
    block.ax.set_ylim([0, 1])

    anim = amp.Animation([block])
    anim.controls()
    return anim
