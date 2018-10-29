from ..animation import Animation
from ..timeline import Timeline
from ..blocks import vector_comp
import numpy as np


def vector_plot(X, Y, U, V, t, skip=5, *, t_axis=0, units='', fps=10,
                pcolor_kw={}, quiver_kw={}):
    """produces an animation of vector fields

    This takes 2D vector field, and plots the magnitude as a pcolomesh, and the
    normalized direction as a quiver plot. It then animates it.

    This is a convience function. It wraps around the Pcolormesh and Quiver
    blocks. It will be more restrictive than using the blocks themselves. If
    you need more control, or the ability to pass data in as a list, then use
    the individual blocks.

    Parameters
    ----------
    X : 2D numpy array
        The x location of the vectors to be animated
    Y : 2D numpy array
        The x location of the vectors to be animated
    U : 3D numpy array
        The x components of the vectors to be animated.
    V : 3D numpy array
        The y components of the vectors to be animated.
    t : 1D numpy array
        The time values
    skip : int, optional
        The amount of values to skip over when making the quiver plot.
        Higher skip means fewer arrows. For best results, the skip should
        divide the length of the data-1. Defaults to 5.
    t_axis : int, optional
        The axis of the U, V array's the represent time. Defaults to 0. Note
        this is different from the defaults that blocks choose. This default
        is chosen to be consistent with 3D-meshgrids (meshgrid(x, y, t)).
    fps : int, optional
        The frames per second to display the animation at.
    units : str, optional
        The units to display on the timeline.
    pcolor_kw : dict, optional
        A dictionary of parameters to pass to pcolormesh.
    quiver_kw : dict, optional
        A dictionary of parameters to pass to quiver.

    Returns
    -------
    Animatplot.Animation
        The complete animation
    list of Animatplot.blocks.Block
        A list of all the blocks used in the animation. The list
        contains a Pcolorblock, and a Quiver block in that order.
    Animatplot.Timeline
        The timeline that was generated for the animation.
    """
    # plot the magnitude of the vectors as a pcolormesh
    blocks = vector_comp(X, Y, U, V, skip, t_axis=t_axis,
                         pcolor_kw=pcolor_kw, quiver_kw=quiver_kw)

    # create the animation
    timeline = Timeline(t, units=units, fps=fps)
    anim = Animation(blocks, timeline)

    return anim, blocks, timeline
