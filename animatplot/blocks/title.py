from string import Formatter

from .base import Block


class Title(Block):
    """Animates an axes title.

    Follows the same syntax as a format-string, but the values to be replaced
    must be given as an array of values for each timestep.

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
        Keyword arguments to pass to matplotlib.pyplot.title()
    args : optional
        Passed on to str.format()
    kwargs : optional
        If kwarg matches a field in the format string, then passed on to
        str.format(), else passed on to matplotlib.axes.Axes.set_title().

    Attributes
    ----------
    ax : matplotlib axis
        The matplotlib axes that the block is attached to.
    """

    def __init__(self, text, ax=None, *args, **kwargs):
        super().__init__(ax)

        if isinstance(text, str):

            # Filter out only the keyword args which are things to be replaced
            # in the title text
            # Parsing trick from https://stackoverflow.com/questions/25996937/
            fieldnames = [fname for _, fname, _, _ in
                          Formatter().parse(text) if fname]
            replacements = {key: value for key, value in kwargs.items()
                            if key in fieldnames}

            # Any leftover kwargs are assumed to be for matplotlib
            mpl_kwargs = {kwarg: kwargs[kwarg] for kwarg in kwargs
                          if kwarg not in fieldnames}
            if mpl_kwargs:
                self._mpl_kwargs = mpl_kwargs
            else:
                self._mpl_kwargs = {}

            if replacements:
                self._length = len(list(replacements.values())[0])
                if not all(len(array) == self._length for array
                           in replacements.values()):
                    raise ValueError("Not all arrays of replacement values are"
                                     " the same length")
            else:
                self._length = 1

            titles = []
            for i in range(self._length):
                replacements_at_one_time = {replacement: array[i]
                                            for replacement, array
                                            in replacements.items()}

                title = text.format(*args, **replacements_at_one_time)
                titles.append(title)
            self.titles = titles

        elif isinstance(text, list):
            if not all(isinstance(x, str) for x in text):
                raise TypeError("Not all the elements in the list given as "
                                "argument text are strings")
            self._length = len(text)
            self.titles = text
            self._mpl_kwargs = kwargs

        else:
            raise TypeError("argument text must be either a string or a list "
                            "of strings")

        # Draw the title for the first frame
        self._update(0)

    def _update(self, i):
        self.text = self.ax.set_title(label=self.titles[i], **self._mpl_kwargs)
        return self.text

    def __len__(self):
        return self._length
