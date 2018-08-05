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


def demeshgrid(arr):
    """Turns an ndarray created by a meshgrid back into a 1D array

    Parameters
    ----------
    arr : array of dimension > 1
        This array should have been created by a meshgrid.
    """
    dim = len(arr.shape)
    for i in range(dim):
        Slice1 = [0]*dim
        Slice2 = [1]*dim
        Slice1[i] = slice(None)
        Slice2[i] = slice(None)
        if (arr[tuple(Slice1)] == arr[tuple(Slice2)]).all():
            return arr[tuple(Slice1)]
