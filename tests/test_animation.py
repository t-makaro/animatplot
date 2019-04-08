from matplotlib.testing import setup
setup()
import os
import pytest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import numpy.testing as npt

import animatplot as amp
from tests.tools import animation_compare


@pytest.mark.xfail
@animation_compare(baseline_images='Animation/controls', nframes=5, tol=.5)
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


@pytest.fixture()
def line_block():
    def make_line_block(t_length=5):
        x = np.linspace(0, 1, 10)
        t = np.linspace(0, 1, t_length)
        x_grid, t_grid = np.meshgrid(x, t)
        y_data = np.sin(2 * np.pi * (x_grid + t_grid))

        return amp.blocks.Line(x, y_data)
    return make_line_block


class TestAdd:
    def test_add_blocks(self, line_block):
        anim = amp.Animation([line_block()])
        anim2 = anim.add(line_block())

        assert isinstance(anim2, amp.Animation)
        assert len(anim2.blocks) == 2
        for actual in anim2.blocks:
            assert len(actual) == 5
            npt.assert_equal(actual.line.get_xdata(),
                             np.linspace(0, 1, 10))

    def test_wrong_length_block(self, line_block):
        anim = amp.Animation([line_block()])

        with pytest.raises(ValueError):
            anim.add(line_block(t_length=6))

    def test_wrong_type(self, line_block):
        anim = amp.Animation([line_block()])

        with pytest.raises(TypeError):
            anim.add('not a block')
