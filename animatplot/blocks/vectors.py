from .base import Block


class Quiver(Block):
    """
    A block for animated quiver plots

    Parameters
    ----------
    X, Y : 2D or 3D numpy array
    U, V : 3D numpy array
    axis : matplotlib axis, optional
        The axis to the block to
    Notes
    -----
    This block accepts additional keyword arguments to be passed to
    :meth:`matplotlib.axes.Axes.quiver`
    """
    def __init__(self, X, Y, U, V, axis=None, **kwargs):
        if X.shape != Y.shape:
            raise ValueError("X, Y must have the same shape")
        if U.shape != V.shape:
            raise ValueError("U, V must have the same shape")

        # lots of features removed b/c quiver plots can't set_XY
        # self.animate_XY = len(X.shape) == 3
        # self.animate_UV = len(U.shape) == 3

        self.x = X
        self.y = Y
        self.u = U
        self.v = V
        self.ax = axis

        xy_slice = [slice(None)]*2 + ([slice(1)] if len(X.shape) == 3 else [])
        # uv_slice = [slice(None)]*2 +([slice(1)] if len(U.shape) == 3 else [])

        self.Q = self.ax.quiver(X[tuple(xy_slice)].squeeze(),
                                Y[tuple(xy_slice)].squeeze(),
                                U[:, :, 0],            V[:, :, 0],
                                **kwargs)

    def _update(self, i):
        # if self.animate_UV:
        self.Q.set_UVC(self.u[:, :, i], self.v[:, :, i])
        # if self.animate_XY:
        #    pass  # self.Q.set_XYC(self.x[:, :, i], self.y[:, :, i])
        return self.Q,

    def __len__(self):
        # if len(self.x.shape) == 3:
        #    return self.x.shape[2]
        # else:
        return self.u.shape[2]
