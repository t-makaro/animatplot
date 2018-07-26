from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider


class Animation:
    """This class handles the actual animating

    Attributes
    ----------
    animation :
        a matplotlib animation returned from FuncAnimation
    """
    def __init__(self, blocks, timeline, fig, init_func=None):

        _len_time = len(timeline)
        for block in blocks:
            if len(block) != _len_time:
                raise "Block not all the same length"

        self.blocks = blocks
        self.timeline = timeline
        self.fig = fig
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
                self.slider.set_val(self.index)
            self.timeline.update()

        self.animation = FuncAnimation(
            self.fig, animate,
            frames=self.timeline._len,
            init_func=init,
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

    def slider(self, ax=None):
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
            self.slider_ax, "Time", 0, self.timeline._len,
            valinit=0,
            valfmt=('%1.2f'+self.timeline.units),
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
