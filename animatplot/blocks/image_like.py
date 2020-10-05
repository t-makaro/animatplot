from .base import Block
import matplotlib.pyplot as plt
import numpy as np


class Pcolormesh(Block):
    """Animates a pcolormesh

    Parameters
    ----------
    X : 1D or 2D np.ndarray, optional
    Y : 1D or 2D np.ndarray, optional
    C : list of 2D np.ndarray or a 3D np.ndarray
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to attach the block to.
        Defaults to matplotlib.pyplot.gca()
    t_axis : int, optional
        The axis of the array that represents time. Defaults to 0.
        No effect if C is a list.

    Attributes
    ----------
    ax : matplotlib axis
        The matplotlib axes that the block is attached to.

    Notes
    -----
    All other keyword arguments get passed to ``axis.pcolormesh``
    see :meth:`matplotlib.axes.Axes.pcolormesh` for details.
    """
    def __init__(self, *args, ax=None, t_axis=0, **kwargs):
        if len(args) == 1:
            self.C = args[0]
            self._arg_len = 1
        elif len(args) == 3:
            self.X, self.Y, self.C = args
            self._arg_len = 3
            if len(self.X.shape) not in [1, 2]:
                raise TypeError('X must be a 1D or 2D arrays')
            if len(self.Y.shape) not in [1, 2]:
                raise TypeError('Y must be a 1D or 2D arrays')
        else:
            raise TypeError(
                'Illegal arguments to pcolormesh; see help(pcolormesh)')

        super().__init__(ax, t_axis)

        self._is_list = isinstance(self.C, list)
        self.C = np.asanyarray(self.C)

        Slice = self._make_slice(0, 3)

        # replicate matplotlib logic for setting default shading value because
        # matplotlib resets the _shading member variable of the QuadMesh to "flat" after
        # interpolating X and Y to corner positions
        self. shading = kwargs.get("shading", plt.rcParams.get("pcolor.shading", "flat"))
        Nx = self.X.shape[-1]
        Ny = self.Y.shape[0]
        if self.shading == "auto":
            if (Ny, Nx) == self.C[Slice].shape:
                self.shading = "nearest"
            else:
                self.shading = "flat"
        if self.shading == "flat" and ((Ny - 1, Nx - 1) == self.C[Slice].shape):
            # Need to slice without the workaround in _update()
            self.shading = "flat_corner_grid"

        if self._arg_len == 1:
            self.quad = self.ax.pcolormesh(self.C[Slice], **kwargs)
        elif self._arg_len == 3:
            self.quad = self.ax.pcolormesh(self.X, self.Y, self.C[Slice], **kwargs)

    def _update(self, i):
        if self.shading == "flat":
            Slice = self._make_pcolormesh_flat_slice(i, 3)
            self.quad.set_array(self.C[Slice].ravel())
        else:
            Slice = self._make_slice(i, 3)
            self.quad.set_array(self.C[Slice])
        return self.quad

    def __len__(self):
        if self._is_list:
            return self.C.shape[0]
        return self.C.shape[self.t_axis]

    def _make_pcolormesh_flat_slice(self, i, dim):
        if self._is_list:
            return i
        Slice = [slice(-1)]*3  # weird thing to make animation work
        Slice[self.t_axis] = i
        return tuple(Slice)


class Imshow(Block):
    """Animates a series of images

    Parameters
    ----------
    images : list of 2D/3D arrays, or a 3D or 4D array
        matplotlib considers arrays of the shape
        (n,m), (n,m,3), and (n,m,4) to be images.
        Images is either a list of arrays of those shapes,
        or an array of shape (T,n,m), (T,n,m,3), or (T,n,m,4)
        where T is the length of the time axis (assuming ``t_axis=0``).
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to attach the block to.
        Defaults to matplotlib.gca()
    t_axis : int, optional
        The axis of the array that represents time. Defaults to 0.
        No effect if images is a list.

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes that the block is attached to.

    Notes
    -----
    This block accepts additional keyword arguments to be passed to
    :meth:`matplotlib.axes.Axes.imshow`
    """
    def __init__(self, images, ax=None, t_axis=0, **kwargs):
        self.ims = np.asanyarray(images)
        super().__init__(ax, t_axis)

        self._is_list = isinstance(images, list)
        self._dim = len(self.ims.shape)

        Slice = self._make_slice(0, self._dim)
        self.im = self.ax.imshow(self.ims[Slice], **kwargs)

    def _update(self, i):
        Slice = self._make_slice(i, self._dim)
        self.im.set_array(self.ims[Slice])
        return self.im

    def __len__(self):
        if self._is_list:
            return self.ims.shape[0]
        return self.ims.shape[self.t_axis]
