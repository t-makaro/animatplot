from matplotlib.testing import setup
setup()
import os
import pytest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import animatplot as amp
from animatplot.testing import animation_compare


# @pytest.mark.xfail
@animation_compare(baseline_images='Animation/controls', nframes=5)
def test_controls():
    x = np.linspace(0, 1, 5)
    y = np.sin(np.pi*x)
    t = np.linspace(0, 1, 5)

    timeline = amp.Timeline(t, units='s', fps=5)
    block = amp.blocks.ParametricLine(x, y)
    block.ax.set_xlim([0, 1])
    block.ax.set_ylim([0, 1])

    anim = amp.Animation([block], timeline)
    anim.controls()
    return anim


def test_save():
    base = 'tests/output_images/'
    if not os.path.exists(base):
        os.mkdir(base)
    x = np.linspace(0, 1, 5)
    y = np.sin(np.pi*x)

    block = amp.blocks.ParametricLine(x, y)
    block.ax.set_xlim([0, 1])
    block.ax.set_ylim([0, 1])

    anim = amp.Animation([block])
    anim.save_gif(base+'save')
    plt.close('all')
    assert os.path.exists(base+'save.gif')
