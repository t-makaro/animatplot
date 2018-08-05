import animatplot.util as util
import numpy as np


def test_parametric_line():
    x = np.arange(5)
    y = x**2

    X_test, Y_test = util.parametric_line(x, y)
    X_valid = np.array(
        [[0, np.nan, np.nan, np.nan, np.nan],
         [0, 1,      np.nan, np.nan, np.nan],
         [0, 1,      2,      np.nan, np.nan],
         [0, 1,      2,      3,      np.nan],
         [0, 1,      2,      3,      4]]
    )
    Y_valid = X_valid**2

    mask = np.isnan(X_test)
    assert (mask == np.isnan(Y_test)).all()
    assert (mask == np.isnan(X_valid)).all()

    assert (X_valid[~mask] == X_test[~mask]).all()
    assert (Y_valid[~mask] == Y_test[~mask]).all()


def test_demeshgrid():
    x = np.linspace(-1, 1, 10)
    t = np.linspace(0, 1, 10)

    _, T = np.meshgrid(x, t)
    assert (util.demeshgrid(T) == t).all()

    _, _, T = np.meshgrid(x, x, t)
    assert (util.demeshgrid(T) == t).all()
