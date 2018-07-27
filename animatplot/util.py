import numpy as np


def parametric_line(x, y):
    """
    Parameters
    ----------
    x : 1D numpy array
    y : 1D numpy array
    """
    if len(x) != len(y):
        raise ValueError("Arrays must be the same length")

    X = np.ones((len(x), len(x)))*np.nan
    Y = X.copy()

    for i in range(len(x)):
        X[i, :(i+1)] = x[:(i+1)]
        Y[i, :(i+1)] = y[:(i+1)]
    return X, Y
