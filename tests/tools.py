import os
from os.path import join, split
import functools
from pathlib import Path
import pytest

import matplotlib.pyplot as plt
from matplotlib.animation import FileMovieWriter
from matplotlib.testing.compare import compare_images
from matplotlib.testing.decorators import remove_ticks_and_titles
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
        super().setup(fig, dpi, frame_prefix)
        self.fname_format_str = '%s%%d.%s'
        self.temp_prefix, self.frame_format = self.outfile.split('.')

    def _frame_sink(self):
        # Creates a filename for saving using the basename and the current
        # counter.
        path = Path(self._base_temp_name() % self._frame_counter)

        # Save the filename so we can delete it later if necessary
        self._temp_paths.append(path)
        self._frame_counter += 1  # Ensures each created name is 'unique'

        # This file returned here will be closed once it's used by savefig()
        # because it will no longer be referenced and will be gc-ed.
        return open(path, 'wb')

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


def _compare_animation(anim, expected, format_, nframes, tol):
    # generate images from the animation
    base_dir, filename = split(join('tests', 'baseline_images', expected))
    out_dir = split(join('tests', 'output_images', expected))[0]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    anim.save(os.path.join(out_dir, (filename+format_)), writer=BunchOFiles())

    for i in range(nframes):
        image_name = '%s%d%s' % (filename, i, format_)
        expected_name = os.path.join(base_dir, image_name)
        actual_name = os.path.join(out_dir, image_name)

        err = compare_images(expected_name, actual_name, tol,
                             in_decorator=True)

        if not os.path.exists(expected_name):
            raise ImageComparisonFailure('image does not exist: %s' % expected_name)

        if err:
            for key in ["actual", "expected"]:
                err[key] = os.path.relpath(err[key])
            raise ImageComparisonFailure(
                'images not close (RMS %(rms).3f):\n\t%(actual)s\n\t%(expected)s ' % err)


def animation_compare(baseline_images, nframes, fmt='.png', tol=1e-3, remove_text=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # First close anything from previous tests
            plt.close('all')

            anim = func(*args, **kwargs)
            if remove_text:
                fignum = plt.get_fignums()[0]
                fig = plt.figure(fignum)
                remove_ticks_and_titles(fig)
            try:
                _compare_animation(anim, baseline_images, fmt, nframes, tol)
            finally:
                plt.close('all')
        return wrapper
    return decorator
