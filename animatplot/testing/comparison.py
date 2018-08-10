import os
from matplotlib.animation import FileMovieWriter
from matplotlib.testing.compare import compare_images
from matplotlib.testing.exceptions import ImageComparisonFailure


class BunchOFiles(FileMovieWriter):
    """
    Exports an animation to a series of images.

    called like:
    ``anim.save('name.format', writer=BunchOFiles())``
    which produces a series of files named ``name{num}.format``
    """
    supported_formats = ['png', 'jpeg', 'bmp', 'svg', 'pdf']

    def __init__(self, *args, extra_args=None, **kwargs):
        # extra_args aren't used but we need to stop None from being passed
        super().__init__(*args, extra_args=(), **kwargs)

    def setup(self, fig, dpi, frame_prefix):
        super().setup(fig, dpi, frame_prefix, clear_temp=False)
        self.fname_format_str = '%s%%d.%s'
        self.temp_prefix, self.frame_format = self.outfile.split('.')

    def grab_frame(self, **savefig_kwargs):
        '''
        Grab the image information from the figure and save as a movie frame.
        All keyword arguments in savefig_kwargs are passed on to the 'savefig'
        command that saves the figure.
        '''

        # Tell the figure to save its data to the sink, using the
        # frame format and dpi.
        with self._frame_sink() as myframesink:
            self.fig.savefig(myframesink, format=self.frame_format,
                             dpi=self.dpi, **savefig_kwargs)

    def finish(self):
        self._frame_sink().close()


def compare_animation(anim, expected, nframes, tol):
    __tracebackhide__ = True
    # generate images from the animation
    anim.save('tests/output_images/' + expected, writer=BunchOFiles())

    name, format = expected.split('.')
    for i in range(nframes):
        image_name = '%s%d.%s' % (name, i, format)
        expected_name = 'tests/baseline_images/' + image_name
        actual_name = 'tests/output_images/' + image_name

        err = compare_images(expected_name, actual_name, tol,
                             in_decorator=True)

        if not os.path.exists(expected_name):
            raise ImageComparisonFailure('image does not exist: %s'
                                         % expected_name)

        if err:
            for key in ["actual", "expected"]:
                err[key] = os.path.relpath(err[key])
            raise ImageComparisonFailure(
                'images not close (RMS %(rms).3f):\n\t%(actual)s\n\t%(expected)s ' % err)
