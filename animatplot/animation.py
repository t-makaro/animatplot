from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.widgets import Button, Slider
from matplotlib.text import Text
import matplotlib.pyplot as plt

import numpy as np

from animatplot import Timeline
from animatplot.blocks.base import Block


class Animation:
    """The foundation of all animations.

    Parameters
    ----------
    blocks : list of animatplot.animations.Block
        A list of blocks to be animated
    timeline : Timeline or 1D array, optional
        If an array is passed in, it will be converted to a Timeline.
        If not given, a timeline will be created using the length of the
        first block.
    fig : matplotlib figure, optional
        The figure that the animation is to occur on

    Attributes
    ----------
    animation
        a matplotlib animation returned from FuncAnimation
    """
    def __init__(self, blocks, timeline=None, fig=None):
        self.fig = plt.gcf() if fig is None else fig

        self.animation = self._animate(blocks, timeline)

    def _animate(self, blocks, timeline):
        if timeline is None:
            self.timeline = Timeline(range(len(blocks[0])))
        elif not isinstance(timeline, Timeline):
            self.timeline = Timeline(timeline)
        else:
            self.timeline = timeline

        _len_time = len(self.timeline)
        for block in blocks:
            if len(block) != _len_time:
                raise ValueError("All blocks must animate for the same amount "
                                 "of time")

        self.blocks = blocks
        self._has_slider = False
        self._pause = False

        def update_all(i):
            updates = []
            for block in self.blocks:
                updates.append(block._update(self.timeline.index))
            if self._has_slider:
                self.slider.set_val(self.timeline.index)
            self.timeline._update()
            return updates

        return FuncAnimation(self.fig, update_all, frames=self.timeline._len,
                             interval=1000 / self.timeline.fps)

    def toggle(self, ax=None):
        """Creates a play/pause button to start/stop the animation

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            The matplotlib axes to attach the button to.
        """
        if ax is None:
            adjust_plot = {'bottom': .2}
            left, bottom, width, height = (.78, .03, .1, .07)
            rect = (left, bottom, width, height)

            plt.subplots_adjust(**adjust_plot)
            self.button_ax = plt.axes(rect)
        else:
            self.button_ax = ax

        self.button = Button(self.button_ax, "Pause")
        self.button.label2 = self.button_ax.text(
            x=0.5, y=0.5, s='Play',
            verticalalignment='center',
            horizontalalignment='center',
            transform=self.button_ax.transAxes
        )
        self.button.label2.set_visible(False)

        def pause(event):
            if self._pause:
                self.animation.event_source.start()
                self.button.label.set_visible(True)
                self.button.label2.set_visible(False)
            else:
                self.animation.event_source.stop()
                self.button.label.set_visible(False)
                self.button.label2.set_visible(True)
            self.fig.canvas.draw()
            self._pause ^= True
        self.button.on_clicked(pause)

    def timeline_slider(self, text='Time', ax=None, valfmt=None, color=None):
        """Creates a timeline slider.

        Parameters
        ----------
        text : str, optional
            The text to display for the slider. Defaults to 'Time'
        ax : matplotlib.axes.Axes, optional
            The matplotlib axes to attach the slider to.
        valfmt : str, optional
            a format specifier used to print the time
            Defaults to '%s' for datetime64, timedelta64 and '%1.2f' otherwise.
        color :
            The color of the slider.
        """

        if valfmt is None:
            if (np.issubdtype(self.timeline.t.dtype, np.datetime64)
               or np.issubdtype(self.timeline.t.dtype, np.timedelta64)):
                valfmt = '%s'
            else:
                valfmt = '%1.2f'
        if self.timeline.log:
            valfmt = '$10^{%s}$' % valfmt

        if ax is None:
            # Try to intelligently decide slider width to avoid overlap

            renderer = self.fig.canvas.get_renderer()

            # Calculate width of widest time value on plot
            def text_width(txt):
                t_val_text = Text(text=txt, figure=self.fig)
                bbox = t_val_text.get_window_extent(renderer=renderer)
                extents = self.fig.transFigure.inverted().transform(bbox)
                return extents[1][0] - extents[0][0]

            text_val_width = max(text_width(valfmt % (self.timeline[i]))
                                 for i in range(len(self.timeline)))
            label_width = text_width(text)

            # Calculate width of slider
            default_button_width = 0.1
            width = 0.73 - text_val_width - label_width - default_button_width

            adjust_plot = {'bottom': .2}
            left, bottom, height = (.18, .05, .03)
            rect = (left, bottom, width, height)

            plt.subplots_adjust(**adjust_plot)
            self.slider_ax = plt.axes(rect)
        else:
            self.slider_ax = ax

        self.slider = Slider(
            self.slider_ax, label=text, valmin=0, valmax=self.timeline._len-1,
            valinit=0,
            valfmt=(valfmt+self.timeline.units),
            valstep=1, color=color
        )
        self._has_slider = True

        def set_time(new_slider_val):
            # Update slider value and text on each step
            self.timeline.index = int(new_slider_val)
            self.slider.valtext.set_text(
                self.slider.valfmt % (self.timeline[self.timeline.index]))

            if self._pause:
                for block in self.blocks:
                    block._update(self.timeline.index)
                self.fig.canvas.draw()

        self.slider.on_changed(set_time)

    def controls(self, timeline_slider_args={}, toggle_args={}):
        """Creates interactive controls for the animation

        Creates both a play/pause button, and a time slider at once

        Parameters
        ----------
        timeline_slider_args : Dict, optional
            A dictionary of arguments to be passed to timeline_slider()
        toggle_args : Dict, optional
            A dictionary of argyments to be passed to toggle()
        """
        self.timeline_slider(**timeline_slider_args)
        self.toggle(**toggle_args)

    def save_gif(self, filename):
        """Saves the animation to a gif

        A convenience function. Provided to let the user avoid dealing
        with writers - uses PillowWriter.

        Parameters
        ----------
        filename : str
            the name of the file to be created without the file extension
        """
        self.timeline.index -= 1  # required for proper starting point for save
        self.animation.save(filename+'.gif',
                            writer=PillowWriter(fps=self.timeline.fps))

    def save(self, *args, **kwargs):
        """Saves an animation

        A wrapper around :meth:`matplotlib.animation.Animation.save`
        """
        self.timeline.index -= 1  # required for proper starting point for save
        self.animation.save(*args, **kwargs)

    def add(self, new):
        """
        Updates the animation object by adding additional blocks.

        The new blocks can be passed as a list, or as part of a second animaion.
        If passed as part of a new animation, the timeline of this new
        animation object will replace the old one.

        Parameters
        ----------
        new : amp.animation.Animation, or list of amp.block.Block objects
            Either blocks to add to animation instance, or another animation
            instance whose blocks should be combined with this animation.
        """

        if isinstance(new, Animation):
            new_blocks = new.blocks
            new_timeline = new.timeline

        else:
            if not isinstance(new, list):
                new_blocks = [new]
            else:
                new_blocks = new
            new_timeline = self.timeline

        for i, block in enumerate(new_blocks):
            if not isinstance(block, Block):
                raise TypeError(f"Block number {i} passed is of type "
                                f"{type(block)}, not of type "
                                f"animatplot.blocks.Block (or a subclass)")

            self.blocks.append(block)

        self.animation = self._animate(self.blocks, new_timeline)
