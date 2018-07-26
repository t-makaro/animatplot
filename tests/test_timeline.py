from numpy import arange, array
from animatplot.timeline import timeline


def test_repr():
    times = arange(0, 5, .5)
    t = timeline(times)

    representation = "timeline(t=array([0. , 0.5, 1. , 1.5, 2. , 2.5, " \
                     "3. , 3.5, 4. , 4.5]), units='', fps=30)"
    assert repr(t) == representation
    assert isinstance(eval(repr(t)), timeline)
