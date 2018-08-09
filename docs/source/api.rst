API
===

Animatplot is build on top of three main classes:

* Animation
* Block
* Timeline

A ``Timeline`` holds the information and logic to actually control the timing of all animations.

A ``Block`` represent any "thing" that is to be animated.

An ``Animation`` is a composition of a list of blocks and a timeline. This class builds the final animation.

.. currentmodule:: animatplot

Animation
---------
.. autosummary::
    :toctree: _as_gen/

    Animation

Timeline
--------
.. autosummary::
    :toctree: _as_gen/

    Timeline

blocks
------

Blocks handle the animation of different types of data.
The following blocks are available in ``animatplot.blocks``.

.. currentmodule:: animatplot.blocks
.. autosummary::
    :toctree: _as_gen/

    Block
    Line
    Quiver
    Pcolormesh
    Imshow
    Nuke

Animatplot.animations
---------------------

The animations subpackge is an opinionated subpackage that contains a number
of convience functions for specific use cases. These functions wrap around different
combinations of blocks.

In general, these functions will take some data to be animated, some parameters to tell 
animatplot what to do, then dictionaries of parameters to pass to the underlying blocks.

.. warning::

    This subpackage may less API stable than the above (blocks/Animation/Timeline), 
    and some of these functions may have different defaults.

This submodule contains the following functions.

.. currentmodule:: animatplot.animations
.. autosummary::
    :toctree: _as_gen/

    vector_plot
