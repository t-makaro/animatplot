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
    title : str or list of str
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

    def __init__(self, title, ax=None, mpl_kwargs=None, *args, **kwargs):
        axis = kwargs.pop('axis', None)
        if axis is not None:
            warn('axis has been replaced in favour of "ax", '
                 'and will be removed in 0.4.0.')
            ax = axis

        super().__init__(ax)

        if isinstance(title, str):
            self._basetitle = title

            # Filter out only the keyword args which are things to be replaced
            # in the title text
            # From https://stackoverflow.com/questions/25996937/
            fieldnames = [fname for _, fname, _, _ in
                          Formatter().parse(title) if fname]
            replacements = {key: value for key, value in kwargs.items()
                            if key in fieldnames}

            # Select the values for the first frame
            initial_replacements = {key: value[0] for key, value
                                    in replacements.items()}

            # Any leftovers are passed to .format
            format_kwargs = {key: value for key, value in kwargs.items()
                            if key not in fieldnames}

            self._titles = [self._basetitle.format(*args, **replacements,
                                                   **format_kwargs)]
            self.ax = ax.title(label=self.text, **mpl_kwargs)

        elif isinstance(title, list):
            if not all(isinstance(text, str) for text in title):
                # TODO ValueError or TypeError?
                raise ValueError
            self._titles = title
            self.text = title[0]

        else:
            raise ValueError("title must be either a string or a list of "
                             "strings")
