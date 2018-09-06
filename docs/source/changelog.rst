Changes to animatplot
=====================

0.3.0
-----

**Deprecations**

- The ``axis`` keyword argument has been replaced in favour of ``ax``. ``axis`` refered to a ``matplotlib.axes.Axes`` which is plural because axes is composed of an x and a y axis, so the singular form made no sense. ``ax`` avoids this problem altogether, and is also consistent with Pandas' plotting wrapper.

**Features**

- The Pcolormesh block now accepts 1D arrays (in addition to 2D) for x and y inputs.
- Animation.timeline_slider now accepts a ``text`` argument to change the name of the slider.
- New (and somewhat experimental) ``animations`` subpackage (well new to the public api). Contains some new convenice functions.

    - ``vector_plot`` wraps Pcolormesh and Quiver to produce animated vector fields.

**Bug Fixes**

- Previously, an Animation with a timeline_slider, but no toggle would cause an error.

**Breaking Changes**

- The ```text``` argument to timeline_slider is now the first positional argument. 

0.2.2
-----
- Fix .animations and .blocks subpackages not being distributed properly. 

0.2.0
-----

- Complete and total overhaul of animatplot using with the idea of ``blocks`` as a foundation
- Chuck all previous attempts to support python 2 in the dumpster

0.1.0.dev3
----------

This is the original release.
