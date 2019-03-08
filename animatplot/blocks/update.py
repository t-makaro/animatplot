from .base import Block


class Update(Block):
    """For providing a custom update method

    This block allows you to write a custom update method to provide
    functionality not available with other blocks.

    Parameters
    ----------
    func : callable
        This function will be called once for each frame of the animation.
        The first argument to this function must be an integer
        representing the frame number. It should return a matplotlib
        artist.
    length : int
        The number of frames to display.
    fargs : list, optional
        A list of arguments to pass into func.
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to which the block is attached.
        Defaults to matplotlib.pyplot.gca()

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes to which the block is attached.
    """
    def __init__(self, func, length, fargs=[], ax=None):
        self.func = func
        self.length = length
        self.fargs = fargs
        super().__init__(ax)

        func(0, *fargs)

    def _update(self, i):
        self.func(i, *self.fargs)

    def __len__(self):
        return self.length


class Nuke(Update):
    """For when the other blocks just won't do:

    This block will clear the axes and redraw using a provided
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
    length : int
        The number of frames to display.
    fargs : list, optional
        A list of arguments to pass into func.
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to which the block is attached.
        Defaults to matplotlib.pyplot.gca()

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes to which the block is attached.
    """
    def _update(self, i):
        self.ax.clear()
        self.func(i, *self.fargs)
