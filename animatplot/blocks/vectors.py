from .base import Block
from .image_like import Pcolormesh
import numpy as np


class Quiver(Block):
    """
    A block for animated quiver plots

    Parameters
    ----------
    X : 1D or 2D numpy array
        The x positions of the arrows. Cannot be animated.
    Y : 1D or 2D numpy array
        The y positions of the arrows. Cannot be animated.
    U : 2D or 3D numpy array
        The U displacement of the arrows. 1 dimension
        higher than the X, Y arrays.
    V : 2D or 3D numpy array
        The V displcement of the arrows. 1 dimension
        higher than the X, Y arrays.
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to the block to.
        Defaults to matplotlib.pyplot.gca()
    t_axis : int, optional
        The axis of the array that represents time. Defaults to 0.
        No effect if U, V are lists.

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes that the block is attached to.

    Notes
    -----
    This block accepts additional keyword arguments to be passed to
    :meth:`matplotlib.axes.Axes.quiver`
    """
    def __init__(self, X, Y, U, V, ax=None, t_axis=0, **kwargs):
        self.X = X
        self.Y = Y
        self.U = np.asanyarray(U)
        self.V = np.asanyarray(V)
        if X.shape != Y.shape:
            raise ValueError("X, Y must have the same shape")
        if self.U.shape != self.V.shape:
            raise ValueError("U, V must have the same shape")

        super().__init__(ax, t_axis)

        self._dim = len(self.U.shape)
        self._is_list = isinstance(U, list)

        Slice = self._make_slice(0, self._dim)
        self.Q = self.ax.quiver(self.X, self.Y,
                                self.U[Slice], self.V[Slice],
                                **kwargs)

    def _update(self, i):
        Slice = self._make_slice(i, self._dim)
        self.Q.set_UVC(self.U[Slice], self.V[Slice])
        return self.Q

    def __len__(self):
        if self._is_list:
            return self.U.shape[0]
        return self.U.shape[self.t_axis]


def vector_comp(X, Y, U, V, skip=5, *, t_axis=0, pcolor_kw={}, quiver_kw={}):
    """produces an animation of vector fields

    This takes 2D vector field, and plots the magnitude as a pcolomesh, and the
    normalized direction as a quiver plot. It then animates it.

    This is a convience function. It wraps around the Pcolormesh and Quiver
    blocks. It will be more restrictive than using the blocks themselves. If
    you need more control, or the ability to pass data in as a list, then use
    the individual blocks.

    Parameters
    ----------
    X : 2D numpy array
        The x location of the vectors to be animated
    Y : 2D numpy array
        The x location of the vectors to be animated
    U : 3D numpy array
        The x components of the vectors to be animated.
    V : 3D numpy array
        The y components of the vectors to be animated.
    skip : int, optional
        The amount of values to skip over when making the quiver plot.
        Higher skip means fewer arrows. For best results, the skip should
        divide the length of the data-1. Defaults to 5.
    t_axis : int, optional
        The axis of the U, V array's the represent time. Defaults to 0. Note
        this is different from the defaults that blocks choose. This default
        is chosen to be consistent with 3D-meshgrids (meshgrid(x, y, t)).
    pcolor_kw : dict, optional
        A dictionary of parameters to pass to pcolormesh.
    quiver_kw : dict, optional
        A dictionary of parameters to pass to quiver.

    Returns
    -------
    list of Animatplot.blocks.Block
        A list of all the blocks used in the animation. The list
        contains a Pcolorblock, and a Quiver block in that order.
    """
    # plot the magnitude of the vectors as a pcolormesh
    magnitude = np.sqrt(U**2+V**2)
    pcolor_block = Pcolormesh(X, Y, magnitude, t_axis=t_axis, **pcolor_kw)

    # use a subset of the data to plot the arrows as a quiver plot.
    xy_slice = tuple([slice(None, None, skip)]*len(X.shape))

    uv_slice = [slice(None, None, skip)]*len(U.shape)
    uv_slice[t_axis] = slice(None)
    uv_slice = tuple(uv_slice)

    quiver_block = Quiver(X[xy_slice], Y[xy_slice],
                          U[uv_slice]/magnitude[uv_slice],
                          V[uv_slice]/magnitude[uv_slice],
                          t_axis=t_axis, **quiver_kw)

    return [pcolor_block, quiver_block]
