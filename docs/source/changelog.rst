.. _changelog:

Changes to animatplot
=====================

0.4.0
-----

**Features**

- New Title block. `#27 <https://github.com/t-makaro/animatplot/pull/27>`_
- x values are now optional in the Line Block. `#29 <https://github.com/t-makaro/animatplot/pull/29/>`_

**Bug Fixes**

- Timeline slider now formats ``np.datetime`` properly by default. `#21 <https://github.com/t-makaro/animatplot/pull/21>`_

**Breaking Changes**

- The x, y inputs to the Line Block are not positional only. `#29 <https://github.com/t-makaro/animatplot/pull/29/>`_
- Removed axis kwargs that deprecated in favor of ax in 0.3.0. `#31 <https://github.com/t-makaro/animatplot/pull/31/>`_

**Developer Changes**

- Testing tools were moving into the tests folder and are no longer a subpackage of animatplot. `#26 <https://github.com/t-makaro/animatplot/pull/26/>`_

**Authors**

- `@t-makaro <https://github.com/t-makaro>`_
- `@TomNicholas* <https://github.com/TomNicholas>`_
- `@dcherian* <https://github.com/dcherian>`_

\* indicates new author in this release.

0.3.0
-----

**Deprecations**

- The ``axis`` keyword argument has been replaced (everywhere) in favour of ``ax``, and ``axis`` will be removed completely in ``0.4.0``. This does not apply to ``t_axis`` which is unchanged. See `#10 <https://github.com/t-makaro/animatplot/pull/10>`_ for rational.

**Features**

- The Pcolormesh block now accepts 1D arrays (in addition to 2D) for x and y inputs.
- Animation.timeline_slider now accepts a ``text`` argument to change the name of the slider.
- New blocks:

    - ``Scatter`` for animating scatter plots. Capable of animating size and position of the points, but not yet the color.
    - ``Update`` a block that accepts a generic function that takes a frame number. Good if another block doesn't already exist for some tasks.

- Composition Blocks: These are functions that return a list of blocks (and maybe a timeline). These are in the blocks subpackage and can be identified by the ``_comp`` suffix.
- New (and very experimental) ``animations`` subpackage (well new to the public api). Contains some new convenice functions.

    - ``vector_plot`` wraps Pcolormesh and Quiver to produce animated vector fields.

**Bug Fixes**

- Previously, an Animation with a timeline_slider, but no toggle would cause an error.

**Breaking Changes**

- The ``text`` argument to timeline_slider is now the first positional argument. 
- The order of positional arguments for the ``Nuke`` block has changed. This was required to give the ``ax`` argument a default.

**Developer Changes**

- New animation unittesting framework
- Tests / doc building now runs on CircleCI.

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
