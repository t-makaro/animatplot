import matplotlib.pyplot as plt


class Block:
    """A base class for blocks"""
    def __init__(self, axis=None, t_axis=None):
        self.ax = axis if axis is not None else plt.gca()
        self.t_axis = t_axis
        self._is_list = False

    def _init(self):
        """initialize the animation.

        To be (optionally) implemented by subclasses
        """
        pass

    def _update(self, i):
        """updates the block to display the corresponding frame i.

        To be implemented by subclasses
        """
        raise NotImplementedError()

    def __len__(self):
        """Returns the length of the 'time' axis"""
        raise NotImplementedError()

    def _make_slice(self, i, dim):
        if self._is_list:
            return i
        Slice = [slice(None)]*dim
        Slice[self.t_axis] = i
        return tuple(Slice)
