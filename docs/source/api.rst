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
    pcolormesh
    imshow