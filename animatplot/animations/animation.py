from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.widgets import Button, Slider
import matplotlib.pyplot as plt


class Animation:
    """This class handles the actual animating

    Attributes
    ----------
    animation :
        a matplotlib animation returned from FuncAnimation
    """
    def __init__(self, blocks, timeline, fig=None, init_func=None):
        """
        Parameters
        ----------
        blocks : list of animatplot.animations.Block
            A list of blocks to be animated.
        timeline : timeline
        """
        _len_time = len(timeline)
        for block in blocks:
            if len(block) != _len_time:
                raise "All blocks must animate for the same amount of time"

        self.blocks = blocks
        self.timeline = timeline
        self.fig = plt.gcf() if fig is None else fig
        self._has_slider = False

        def init():
            """FuncAnimation will use this to inialize the plots"""
            if init_func is not None:
                init_func()
            for block in self.blocks:
                block.init()

        def animate(i):
            updates = []
            for block in self.blocks:
                updates.append(block.update(self.timeline.index))
            if self._has_slider:
                self.slider.set_val(self.timeline.index)
            self.timeline.update()
            return updates

        self.animation = FuncAnimation(
            self.fig, animate,
            frames=self.timeline._len,
            # init_func=init,
            interval=1000/timeline.fps
        )

    def toggle(self, ax=None):
        """Creates a play/pause button to start/stop the animation"""
        self._pause = False

        if ax is None:
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

    def timeline_slider(self, ax=None, valfmt='%1.2f'):
        """Create a timeline slider.

        Parameters
        ----------
        ax : maplitlib.axes.Axes
            A matplotlib axis to attach the slider to
        """
        if ax is None:
            adjust_plot = {'bottom': .2}
            rect = [.18, .05, .5, .03]

            plt.subplots_adjust(**adjust_plot)
            self.slider_ax = plt.axes(rect)
        else:
            self.slider_ax = ax

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

    def savegif(self, name):
        """Save the animation to a gif

        A convience function. Provided to let the user avoid dealing
        with writers.

        Parameters
        ----------
        name : str
            the name of the file to be created without the file extension
        """
        self.animation.save(
            name+'.gif',
            writer=PillowWriter(fps=self.timeline.fps)
        )

    def save(self, *args, **kwargs):
        """Saves a figure

        A wrapper around matplotlib's animation.save()
        """
        self.animation.save(*args, **kwargs)
