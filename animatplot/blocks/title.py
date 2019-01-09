from string import Formatter
from warnings import warn

import matplotlib.pyplot as plt

from .base import Block


class Title(Block):
    """Animates an axes title.

    Follows the same syntax as a format-string.

    Alternatively can just accept a list of strings, one for each timestep.

    Parameters
    ----------
    text : str or list of str
        Text to display as the title.
        Either supplied as a list of strings, one for each timestep, or as a
        base string with curly braces for any "replacement fields".
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to attach the block to.
        Defaults to matplotlib.pyplot.gca()
    mpl_kwargs: dict, optional
        Keyword arguments to pass to matplotlib.pyplot.ax.title()
    args : optional
        Passed on to str.format()
    kwargs : optional
        Passed on to str.format()

    Attributes
    ----------
    ax : matplotlib axis
        The matplotlib axes that the block is attached to.
    """

    def __init__(self, text, ax=None, mpl_kwargs=None, *args, **kwargs):
        axis = kwargs.pop('axis', None)
        if axis is not None:
            warn('axis has been replaced in favour of "ax", '
                 'and will be removed in 0.4.0.')
            ax = axis

        super().__init__(ax)

        if isinstance(text, str):
            self._basetitle = text

            # Filter out only the keyword args which are things to be replaced
            # in the title text
            # Parsing trick from https://stackoverflow.com/questions/25996937/
            fieldnames = [fname for _, fname, _, _ in
                          Formatter().parse(text) if fname]
            replacements = {key: value for key, value in kwargs.items()
                            if key in fieldnames}

            length = len(list(replacements.values())[0])
            if not all(len(array) == length for array in replacements.values()):
                raise ValueError("Not all arrays of replacement values are the"
                                 " same length")

            # Any leftover kwargs are to be passed to .format
            format_kwargs = {key: value for key, value in kwargs.items()
                            if key not in fieldnames}

            titles = []
            for i in range(length):
                replacements_at_one_time = {replacement: array[i]
                                            for replacement, array
                                            in replacements.items()}

                title = self._basetitle.format(*args, **format_kwargs,
                                               **replacements_at_one_time)
                titles.append(title)
            self.titles = titles

        elif isinstance(text, list):
            if not all(isinstance(x, str) for x in text):
                # TODO ValueError or TypeError?
                raise ValueError
            self.titles = text

        else:
            raise ValueError("title must be either a string or a list of "
                             "strings")

        # Select the title for the first frame
        self.text = text[0]

        #self.ax = ax.title(label=self.titles[0], **mpl_kwargs)
