from .base import Block
from warnings import warn


class Nuke(Block):
    """For when the other blocks just won't do

    The block will clear the axes and redraw using a provided
    function on every frame.
    This block can be used with other blocks so long as other
    blocks are attached to a different axes.

    Only use this block as a last resort. Using the block
    is like nuking an ant hill. Hence the name.

    Parameters
    ----------
    func : callable
        The first argument to this function must be an integer
        representing the frame number.
    ax : a matplotlib.axes.Axes, optional
        The matplotlib axes to attach the block to.
        Defaults to matplotlib.pyplot.gca()
    length : int
        the number of frames to display
    fargs : list, optional
        a list of arguments to pass into func

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes that the block is attached to.
    """
    def __init__(self, func, length, fargs=[], ax=None, axis=None):
        if axis is not None:
            warn('axis has been replaced in favour of "ax", '
                 'and will be removed in a 0.4.0.')
            ax = axis
        self.func = func
        self.length = length
        self.fargs = fargs
        super().__init__(ax)

        func(0, *fargs)

    def _update(self, i):
        self.ax.clear()
        self.func(i, *self.fargs)

    def __len__(self):
        return self.length
