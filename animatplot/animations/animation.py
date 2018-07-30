from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.widgets import Button, Slider
import matplotlib.pyplot as plt


class Animation:
    """The foundation of all animations.

    Parameters
    ----------
    blocks : list of animatplot.animations.Block
        A list of blocks to be animated
    timeline : timeline
    fig : matplotlib figure, optional
        The figure that the animation is to occur on

    Attributes
    ----------
    animation
        a matplotlib animation returned from FuncAnimation
    """
    def __init__(self, blocks, timeline, fig=None):
        _len_time = len(timeline)
        for block in blocks:
            if len(block) != _len_time:
                raise ValueError(
                    "All blocks must animate for the same amount of time")

        self.blocks = blocks
        self.timeline = timeline
        self.fig = plt.gcf() if fig is None else fig
        self._has_slider = False

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
            interval=1000/timeline.fps
        )

    def toggle(self, axis=None):
        """Creates a play/pause button to start/stop the animation

        Parameters
        ----------
        axis : optional
            A matplotlib axis to attach the button to.
        """
        self._pause = False

        if axis is None:
            adjust_plot = {'bottom': .2}
            rect = [.78, .03, .1, .07]

            plt.subplots_adjust(**adjust_plot)
            self.button_ax = plt.axes(rect)
        else:
            self.button_ax = axis

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

    def timeline_slider(self, axis=None, valfmt='%1.2f'):
        """Create a timeline slider.

        Parameters
        ----------
        axis : optional
            A matplotlib axis to attach the slider to
        valfmt : str
            a format specifier use to print the time
        """
        if axis is None:
            adjust_plot = {'bottom': .2}
            rect = [.18, .05, .5, .03]

            plt.subplots_adjust(**adjust_plot)
            self.slider_ax = plt.axes(rect)
        else:
            self.slider_ax = axis

        self.slider = Slider(
            self.slider_ax, "Time", 0, self.timeline._len-1,
            valinit=0,
            valfmt=(valfmt+self.timeline.units),
            valstep=1
        )
        self._has_slider = True

        def set_time(t):
            self.timeline.index = int(self.slider.val)
            self.slider.valtext.set_text(
                self.slider.valfmt % (self.timeline[self.timeline.index]))
            if self._pause:
                for block in self.blocks:
                    block.update(self.timeline.index)
                self.fig.canvas.draw()
        self.slider.on_changed(set_time)

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
        self.animation.save(
            filename+'.gif',
            writer=PillowWriter(fps=self.timeline.fps)
        )

    def save(self, *args, **kwargs):
        """Saves an animation

        A wrapper around :meth:`matplotlib.animation.Animation.save`
        """
        self.timeline.index -= 1  # required for proper starting point for save
        self.animation.save(*args, **kwargs)
