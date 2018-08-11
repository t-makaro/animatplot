import pytest
import numpy as np
from numpy import arange, array
from animatplot.timeline import Timeline


def test_repr():
    times = arange(0, 5, .5)
    t = Timeline(times)

    representation = "Timeline(t=array([0. , 0.5, 1. , 1.5, 2. , 2.5, " \
                     "3. , 3.5, 4. , 4.5]), units='', fps=10)"
    assert repr(t) == representation
    assert isinstance(eval(repr(t)), Timeline)


def test_parse():
    t = np.linspace(.1, 1, 10)
    T, T = np.meshgrid(t, t)

    timeline1 = Timeline(t)
    timeline2 = Timeline(T)
    timeline3 = Timeline(t, log=True)

    assert (timeline1.t == timeline2.t).all()
    assert (timeline3.t == np.log10(t)).all()

    with pytest.raises(ValueError):
        Timeline(np.random.rand(3, 4))
