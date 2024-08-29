from matplotlib.testing import setup
setup()
import os
import pytest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
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
def line_anim():
    def make_line_anim(t_length=5, timeline=False, controls=False):
        x = np.linspace(0, 1, 10)
        t = np.linspace(0, 1, t_length)
        x_grid, t_grid = np.meshgrid(x, t)
        y_data = np.sin(2 * np.pi * (x_grid + t_grid))

        block = amp.blocks.Line(x, y_data)

        if timeline:
            anim = amp.Animation([block], timeline=amp.Timeline(t))
        else:
            anim = amp.Animation([block])

        if controls:
            anim.controls()

        return anim
    return make_line_anim


class TestSlider:
    def test_slider_size(self, line_anim):
        """Test text not overlapping with button (GH issue #32)"""
        anim = line_anim(timeline=True, controls=True)

        slider_rhs = anim.slider_ax.get_position().x1

        valtext_bbox = anim.slider.valtext.get_window_extent()
        valtext_extents = anim.fig.transFigure.inverted().transform(valtext_bbox)
        valtext_rhs = valtext_extents[1][0]

        button_lhs = anim.button_ax.get_position().x0

        assert slider_rhs < button_lhs
        assert valtext_rhs < button_lhs
