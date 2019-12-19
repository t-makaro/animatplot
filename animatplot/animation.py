from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button, Slider
import matplotlib.pyplot as plt
import numpy as np

from animatplot import Timeline


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
        if timeline is None:
            self.timeline = Timeline(range(len(blocks[0])))
        elif not isinstance(timeline, Timeline):
            self.timeline = Timeline(timeline)
        else:
            self.timeline = timeline

        _len_time = len(self.timeline)
        for block in blocks:
            if len(block) != _len_time:
                raise ValueError("All blocks must animate for the same amount of time")

        self.blocks = blocks
        self.fig = plt.gcf() if fig is None else fig
        self._has_slider = False
        self._pause = False
        self._controls_gridspec_object = None

        def animate(i):
            updates = []
            for block in self.blocks:
                updates.append(block._update(self.timeline.index))
            if self._has_slider:
                self.slider.set_val(self.timeline.index)
            self.timeline._update()
            return updates

        self.animation = FuncAnimation(
            self.fig, animate,
            frames=self.timeline._len,
            interval=1000/self.timeline.fps
        )

    @property
    def _controls_gridspec(self):
        if self._controls_gridspec_object is None:
            # make the bottom of the subplots grid lower to fit the controls in
            adjust_plot = {'bottom': 0.03}
            plt.subplots_adjust(**adjust_plot)

            controls_height = 0.2

            fig_gridspecs = self.fig._gridspecs
            if len(fig_gridspecs) > 1:
                raise ValueError('multiple gridspecs found in figure')
            gs = fig_gridspecs[0]
            nrows, ncols = gs.get_geometry()
            height_ratios = gs.get_height_ratios()

            # update parameters with a new row
            if height_ratios is None:
                # if height_ratios is None, all rows on the original gridspec
                # are the same height
                height_ratios = [(1.-controls_height)/nrows
                                 for i in range(nrows)]
            else:
                height_ratios = [r*(1.-controls_height) for r in height_ratios]
            height_ratios.append(controls_height)
            gs._nrows += 1
            gs.set_height_ratios(height_ratios)

            # make a sub-grid in the bottom row
            self._controls_gridspec_object = gs[-1, :].subgridspec(
                    1,3, width_ratios=[.07, .65, .28], wspace=0., hspace=0.)
            gs.update()

        return self._controls_gridspec_object

    def toggle(self, ax=None):
        """Creates a play/pause button to start/stop the animation

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            The matplotlib axes to attach the button to.
        """
        if ax is None:
            try:
                button_subplotspec = self._controls_gridspec[0, 2]
                button_gridspec = button_subplotspec.subgridspec(
                        3, 3, width_ratios=[0.45, 0.45, 0.1],
                        height_ratios=[.05, .5, .45], wspace=0., hspace=0.)
                self.button_ax = self.fig.add_subplot(button_gridspec[1,1])
            except:
                # editing the gridspec did not work for some reason, fall back to
                # subplots_adjust
                print('warning: adding play/pause button to gridspec failed, '
                      'adding in independent axes. tight_layout() will ignore '
                      'the button.')
                adjust_plot = {'bottom': .2}
                rect = [.78, .03, .1, .07]

                plt.subplots_adjust(**adjust_plot)
                self.button_ax = plt.axes(rect)
        else:
            self.button_ax = ax

        self.button = Button(self.button_ax, "Pause")
        self.button.label2 = self.button_ax.text(
            0.5, 0.5, 'Play',
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
        if ax is None:
            try:
                slider_subplotspec = self._controls_gridspec[0, 1]
                slider_gridspec = slider_subplotspec.subgridspec(
                        3, 1, height_ratios=[.2, .2, .6], wspace=0.,
                        hspace=0.)
                self.slider_ax = self.fig.add_subplot(slider_gridspec[1, 0])
            except:
                # editing the gridspec did not work for some reason, fall back to
                # subplots_adjust
                print('warning: adding timeline slider to gridspec failed, '
                      'adding in independent axes. tight_layout() will ignore '
                      'the slider.')
                adjust_plot = {'bottom': .2}
                rect = [.18, .05, .5, .03]
                plt.subplots_adjust(**adjust_plot)
                self.slider_ax = plt.axes(rect)
        else:
            self.slider_ax = ax

        if valfmt is None:
            if (np.issubdtype(self.timeline.t.dtype, np.datetime64)
               or np.issubdtype(self.timeline.t.dtype, np.timedelta64)):
                valfmt = '%s'
            else:
                valfmt = '%1.2f'

        if self.timeline.log:
            valfmt = '$10^{%s}$' % valfmt

        self.slider = Slider(
            self.slider_ax, text, 0, self.timeline._len-1,
            valinit=0,
            valfmt=(valfmt+self.timeline.units),
            valstep=1, color=color
        )
        self._has_slider = True

        def set_time(t):
            self.timeline.index = int(self.slider.val)
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

        A convience function. Provided to let the user avoid dealing
        with writers.

        Parameters
        ----------
        filename : str
            the name of the file to be created without the file extension
        """
        self.timeline.index -= 1  # required for proper starting point for save
        self.animation.save(filename+'.gif', writer=PillowWriter(fps=self.timeline.fps))

    def save(self, *args, **kwargs):
        """Saves an animation

        A wrapper around :meth:`matplotlib.animation.Animation.save`
        """
        self.timeline.index -= 1  # required for proper starting point for save
        self.animation.save(*args, **kwargs)
