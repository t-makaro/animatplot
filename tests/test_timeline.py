from numpy import arange, array
from animatplot.timeline import Timeline


def test_repr():
    times = arange(0, 5, .5)
    t = Timeline(times)

    representation = "Timeline(t=array([0. , 0.5, 1. , 1.5, 2. , 2.5, " \
                     "3. , 3.5, 4. , 4.5]), units='', fps=10)"
    assert repr(t) == representation
    assert isinstance(eval(repr(t)), Timeline)
