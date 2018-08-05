from .base import Block


class Pcolormesh(Block):
    """Animates a pcolormesh

    Parameters
    ----------
    X, Y : 2D np.ndarray, optional
    C : 3D np.ndarray
    axis : matplotlib axis

    Notes
    -----
    All other keyword arguments get passed to ``axis.pcolormesh``
    see :meth:`matplotlib.axes.Axes.pcolormesh` for details.
    """
    def __init__(self, *args, axis, **kwargs):
        if len(args) == 1:
            self.C = args[0]
            self._arg_len = 1
        elif len(args) == 3:
            self.X, self.Y, self.C = args
            self._arg_len = 3
            if len(self.X.shape) != 2 or len(self.Y.shape) != 2:
                raise TypeError('X, Y must be 2D arrays')
        else:
            raise TypeError(
                'Illegal arguments to pcolormesh; see help(pcolormesh)')
        if len(self.C.shape != 3):
            raise TypeError('C must be a 3D array')

        super().__init__(axis)

        if self._arg_len == 1:
            self.quad = axis.pcolormesh(self.C[:, :, 0], **kwargs)
        elif self._arg_len == 3:
            self.quad = axis.pcolormesh(self.X, self.Y, self.C[:, :, 0],
                                        **kwargs)

    def _update(self, i):
        if self._arg_len == 1:
            self.quad.set_array(self.C[:, :, i])
        else:
            self.quad.set_array(self.X, self.Y, self.C[:, :, i])
        return self.quad

    def __len__(self):
        return self.C.shape[2]


class Imshow(Block):
    def __init__(self, X, axis, **kwargs):
        self.X = X
        super().__init__(axis)

        im_slice = [slice(None)]*(len(X.shape)-1) + [slice(1)]
        self.im = self.ax.imshow(X[im_slice], **kwargs)

    def _update(self, i):
        im_slice = [slice(None)]*(len(self.X.shape)-1) + [slice(i)]
        self.im.set_array(self.X[im_slice])

    def __len__(self):
        return self.X.shape[-1]
