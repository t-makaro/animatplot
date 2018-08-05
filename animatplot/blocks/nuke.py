from .base import Block


class Nuke(Block):
    """For when the other blocks just won't do

    The block will clear the axis and redraw using a provided
    function on every frame.
    This block can be used with other blocks so long as other
    blocks are attached to a different axis.

    Parameters
    ----------
    func : callable
        The first argument to this function must be an integer
        representing the frame number.
    axis : a matplotlib axis, optional
    length : int
        the number of frames to display
    fargs : list, optional
        a list of arguments to pass into func
    """
    def __init__(self, func, axis, length, fargs=[]):
        self.func = func
        self.length = length
        self.fargs = fargs
        super().__init__(axis)

        func(0, *fargs)

    def _update(self, i):
        self.ax.clear()
        self.func(i, *self.fargs)

    def __len__(self):
        return self.length
