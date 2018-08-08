import animatplot as amp
import xarray as xr


def animated_plot(da, anim_over='__guess__', x='x', y='y', plot_type='imshow', fps=10):
    """
    Function to plot an animated plot from an xarray DataArray.

    The intention is that this would form the basis of a xr.DataArray.plot.animate() method.
    """

    if not isinstance(da, xr.DataArray):
        raise TypeError('First argument must be an xarray DataArray object')

    timeline, evolving_coord = _timeline_from_coords(da.coords, anim_over, fps)
    t_axis = da.dims.index(evolving_coord)

    if len(da.dims) is not 3:
        raise NotImplementedError('Currently only plots 2D dataarrays')

    if plot_type is 'imshow':
        # TODO ideally the blocks method should call the xarray plotting method da.plot.imshow()
        print(da.values.shape)
        print(t_axis)
        block = amp.blocks.Imshow(da.values, t_axis=t_axis)
    else:
        # TODO deal with other kinds of plot (lines, quiver...) here
        raise NotImplementedError('Currently only plots using imshow')

    # TODO if we can't call the xarray plotting method directly then add titles, axes labels etc here
    anim = amp.Animation([block])

    return anim, block, timeline


def _timeline_from_coords(coords, anim_over, fps):
    """Create the animatplot Timeline object from the information in the coordinates attribute of the DataArray."""

    # Determine coordinate over which plot should be animated
    if anim_over is '__guess__':
        # Attempt to automatically determine coordinate over which to animate plot
        guesses = {'t', 'T', 'time', 'Time'}
        matches = list(guesses & set(coords))
        if len(matches) is 1:
            evolving_coord = matches[0]
        else:
            raise ValueError('Could not automatically determine coordinate to animate over - '
                             'multiple possibilities found: ' + str(matches))
    elif anim_over in coords:
        evolving_coord = anim_over
    else:
        raise ValueError('Could not determine coordinate to animate over')

    print(evolving_coord)
    t = coords[evolving_coord].values

    # TODO Attempt to determine units from metadata in dataarray attributes, according to CF conventions

    timeline = amp.Timeline(t, units=None, fps=fps)

    return timeline, evolving_coord
