API
===

Animatplot is build on top of three main classes:

* Animation
* Block
* Timeline

A ``Timeline`` holds the information and logic to actually control the timing of all animations.

A ``Block`` represents any "thing" that is to be animated.

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

Data blocks
~~~~~~~~~~~

These blocks are built to animate data.

.. currentmodule:: animatplot.blocks
.. autosummary::
    :toctree: _as_gen/

    Line
    Quiver
    Pcolormesh
    Imshow
    Scatter
    Surface

Graph Label Blocks
~~~~~~~~~~~~~~~~~~

These blocks are for animating non-data features on an axis.

.. autosummary::
    :toctree: _as_gen/

    Title

Advanced Blocks
~~~~~~~~~~~~~~~

These blocks are for more advanced use. These allow you to write more custom animations.

.. autosummary::
    :toctree: _as_gen/

    Block
    Update
    Nuke

Composition Blocks
~~~~~~~~~~~~~~~~~~

These blocks are amalgamations of other blocks. These are actually functions that return lists of blocks.

.. autosummary::
    :toctree: _as_gen/

    vector_comp

Animatplot.animations
---------------------

The animations subpackage is an opinionated subpackage that contains a number
of convenience functions for specific use cases. These functions wrap around different
combinations of blocks.

In general, these functions will take some data to be animated, some parameters to tell 
animatplot what to do, then dictionaries of parameters to pass to the underlying blocks.

.. warning::

    This subpackage is less API stable than the above (blocks/Animation/Timeline), 
    and some of these functions may have different defaults.

This submodule contains the following functions.

.. currentmodule:: animatplot.animations
.. autosummary::
    :toctree: _as_gen/

    vector_plot
