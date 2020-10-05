from matplotlib.testing import setup
import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt
import matplotlib as mpl
import packaging.version

import pytest

import animatplot as amp
from tests.tools import animation_compare

from animatplot.blocks import Block, Title

setup()


class TestTitleBlock:
    def test_list_of_str(self):
        labels = ['timestep 0', 'timestep 1']
        result = Title(labels)
        assert labels == result.titles
        assert len(result) == 2

    def test_invalid_input(self):
        with pytest.raises(TypeError):
            Title(0)
        with pytest.raises(TypeError):
            Title([6, 7])

    def test_format_str(self):
        actual = Title('timestep {num}', num=[1, 2]).titles
        assert actual == ['timestep 1', 'timestep 2']

        actual = Title('timestep {num}', num=[1]).titles
        assert actual == ['timestep 1']

    def test_no_replacements(self):
        actual = Title('Name').titles
        assert actual == ['Name']

    def test_multiple_replacements(self):
        actual = Title('timestep {num}, max density {n}',
                       num=[1, 2], n=[500, 10]).titles
        expected = ['timestep {num}, max density {n}'.format(num=1, n=500),
                    'timestep {num}, max density {n}'.format(num=2, n=10)]
        assert actual == expected

    def test_string_formatting(self):
        actual = Title('timestep {values:.2f}', values=[5e7]).titles
        assert actual == ['timestep 50000000.00']

    def test_format_str_numpy_arrays(self):
        actual = Title('timestep {num}', num=np.array([1, 2])).titles
        assert actual == ['timestep 1', 'timestep 2']

    # Hypothesis test that the strings are always formatted correctly?

    def test_text(self):
        # TODO test that the right type of object is produced?
        title_block = Title('timestep {num}', num=[1, 2])

        ax = plt.gca()
        assert ax.get_title() == 'timestep 1'
        title_block._update(1)
        assert ax.get_title() == 'timestep 2'
        plt.close('all')

    def test_mpl_kwargs(self):
        expected = {'loc': 'left', 'fontstyle': 'italic'}
        actual = Title('timestep {num}', num=[1, 2], **expected)
        assert actual._mpl_kwargs == expected


def assert_jagged_arrays_equal(x, y):
    for x, y in zip(x, y):
        npt.assert_equal(x, y)


class TestLineBlock:
    def test_2d_inputs(self):
        x = np.linspace(0, 1, 10)
        t = np.linspace(0, 1, 5)
        x_grid, t_grid = np.meshgrid(x, t)
        y_data = np.sin(2 * np.pi * (x_grid + t_grid))

        line_block = amp.blocks.Line(x_grid, y_data)

        assert isinstance(line_block, amp.blocks.Line)
        npt.assert_equal(line_block.x, x_grid)
        npt.assert_equal(line_block.y, y_data)
        assert len(line_block) == len(t)

        assert isinstance(line_block.line, mpl.lines.Line2D)
        xdata, ydata = line_block.line.get_data()
        npt.assert_equal(xdata, x)
        npt.assert_equal(ydata, y_data[0, :])

    def test_update(self):
        x = np.linspace(0, 1, 10)
        t = np.linspace(0, 1, 5)
        x_grid, t_grid = np.meshgrid(x, t)
        y_data = np.sin(2 * np.pi * (x_grid + t_grid))

        line_block = amp.blocks.Line(x_grid, y_data)
        line_block._update(frame=1)

        npt.assert_equal(line_block.line.get_xdata(), x)
        npt.assert_equal(line_block.line.get_ydata(), y_data[1, :])

    def test_constant_x(self):
        x = np.linspace(0, 1, 10)
        t = np.linspace(0, 1, 5)
        x_grid, t_grid = np.meshgrid(x, t)
        y_data = np.sin(2 * np.pi * (x_grid + t_grid))

        line_block = amp.blocks.Line(x, y_data)

        npt.assert_equal(line_block.line.get_xdata(), x)
        npt.assert_equal(line_block.x[-1], x)

    def test_no_x_input(self):
        x = np.linspace(0, 1, 10)
        t = np.linspace(0, 1, 5)
        x_grid, t_grid = np.meshgrid(x, t)
        y_data = np.sin(2 * np.pi * (x_grid + t_grid))

        line_block = amp.blocks.Line(y_data)

        expected_x = np.arange(10)
        npt.assert_equal(line_block.line.get_xdata(), expected_x)

    def test_list_input(self):
        x_data = [np.array([1, 2, 3]), np.array([1, 2, 3])]
        y_data = [np.array([5, 6, 7]), np.array([4, 2, 9])]
        line_block = amp.blocks.Line(x_data, y_data)
        npt.assert_equal(line_block.y, np.array([[5, 6, 7], [4, 2, 9]]))
        npt.assert_equal(line_block.x, np.array([[1, 2, 3], [1, 2, 3]]))

    def test_ragged_list_input(self):
        x_data = [np.array([1, 2, 3]), np.array([1, 2, 3, 4])]
        y_data = [np.array([5, 6, 7]), np.array([4, 2, 9, 10])]

        with pytest.raises(ValueError) as err:
            line_block = amp.blocks.Line(y_data)
        assert "Must specify x data explicitly" in str(err)

        line_block = amp.blocks.Line(x_data, y_data)

        assert_jagged_arrays_equal(line_block.x, np.array(x_data))
        assert_jagged_arrays_equal(line_block.y, np.array(y_data))

    def test_bad_ragged_list_input(self):
        x_data = np.array([np.array([1, 2, 3]), np.array([1, 2, 3, 4])])
        y_data = np.array([np.array([5, 6, 7]), np.array([4, 2, 9, 10, 11])])

        with pytest.raises(ValueError) as err:
            line_block = amp.blocks.Line(x_data, y_data)
        assert "x & y data must match" in str(err)

    def test_bad_input(self):
        # incorrect number of args
        with pytest.raises(ValueError) as err:
            amp.blocks.Line(1, 2, 3)
        assert 'Invalid data arguments' in str(err.value)
        with pytest.raises(ValueError) as err:
            amp.blocks.Line()
        assert 'Invalid data arguments' in str(err.value)

        # No y data
        with pytest.raises(ValueError) as err:
            amp.blocks.Line(np.arange(5), None)
        assert 'Must supply y data' in str(err.value)
        with pytest.raises(ValueError) as err:
            amp.blocks.Line(None)
        assert 'Must supply y data' in str(err.value)

        # y data not 2d
        with pytest.raises(ValueError) as err:
            amp.blocks.Line(np.arange(5), np.random.randn(5, 2, 2))
        assert 'y data must be 2-dimensional' in str(err.value)

        # 1d x doesn't match y
        with pytest.raises(ValueError) as err:
            amp.blocks.Line(np.arange(5), np.random.randn(4, 2))
        assert 'dimensions of x must be compatible' in str(err.value)

        # 2d x doesn't match y
        with pytest.raises(ValueError) as err:
            x = np.array([np.arange(5), np.arange(5)])
            amp.blocks.Line(x, np.random.randn(4, 2), t_axis=1)
        assert 'dimensions of x must be compatible' in str(err.value)

    def test_kwarg_throughput(self):
        x = np.array([np.arange(5), np.arange(5)])
        line_block = amp.blocks.Line(x, np.random.randn(2, 5), t_axis=1,
                                     alpha=0.5)
        assert line_block.line.get_alpha() == 0.5


class TestComparisons:
    @animation_compare(baseline_images='Blocks/Line', nframes=5)
    def test_Line(self):
        x = np.linspace(0, 2*np.pi, 20)
        t = np.linspace(0, 2*np.pi, 5)

        X, T = np.meshgrid(x, t)
        Y = np.sin(X+T)
        block = amp.blocks.Line(X, Y)
        return amp.Animation([block])

    @animation_compare(baseline_images='Blocks/Pcolormesh', nframes=3)
    def test_Pcolormesh(self):
        x = np.linspace(-2*np.pi, 2*np.pi, 100)
        t = np.linspace(0, 2*np.pi, 3)

        X, Y, T = np.meshgrid(x, x, t)
        Z = np.sin(X**2+Y**2-T)

        block = amp.blocks.Pcolormesh(X[:, :, 0], Y[:, :, 0], Z, t_axis=2)
        return amp.Animation([block])

    @animation_compare(baseline_images='Blocks/Pcolormesh_corner', nframes=3)
    def test_Pcolormesh_corner_positions(self):
        # Test with size of Z being (nx-1)*(ny-1) like matplotlib expects for 'flat'
        # shading
        x = np.linspace(-2*np.pi, 2*np.pi, 10)
        t = np.linspace(0, 2*np.pi, 3)

        X, Y, T = np.meshgrid(x, x, t)
        Z = np.sin(X**2+Y**2-T)[:-1, :-1, :]

        block = amp.blocks.Pcolormesh(X[:, :, 0], Y[:, :, 0], Z, t_axis=2)
        return amp.Animation([block])

    @pytest.mark.skipif(
        packaging.version.parse(mpl.__version__) < packaging.version.parse("3.3.0"),
        reason="matplotlib version too low - does not have shading='nearest'"
    )
    @animation_compare(baseline_images='Blocks/Pcolormesh_nearest', nframes=3)
    def test_Pcolormesh_nearest(self):
        x = np.linspace(-2*np.pi, 2*np.pi, 100)
        t = np.linspace(0, 2*np.pi, 3)

        X, Y, T = np.meshgrid(x, x, t)
        Z = np.sin(X**2+Y**2-T)

        block = amp.blocks.Pcolormesh(
            X[:, :, 0], Y[:, :, 0], Z, t_axis=2, shading="nearest"
        )
        return amp.Animation([block])

    @pytest.mark.skipif(
        packaging.version.parse(mpl.__version__) < packaging.version.parse("3.3.0"),
        reason="matplotlib version too low - does not have shading='nearest'"
    )
    @animation_compare(baseline_images='Blocks/Pcolormesh_auto', nframes=3)
    def test_Pcolormesh_nearest(self):
        x = np.linspace(-2*np.pi, 2*np.pi, 10)
        t = np.linspace(0, 2*np.pi, 3)

        X, Y, T = np.meshgrid(x, x, t)
        Z = np.sin(X**2+Y**2-T)

        block = amp.blocks.Pcolormesh(
            X[:, :, 0], Y[:, :, 0], Z, t_axis=2, shading="auto"
        )
        return amp.Animation([block])

    @pytest.mark.skipif(
        packaging.version.parse(mpl.__version__) < packaging.version.parse("3.3.0"),
        reason="matplotlib version too low - shading='gouraud' does not work before 3.3"
    )
    @animation_compare(baseline_images='Blocks/Pcolormesh_gouraud', nframes=1)
    def test_Pcolormesh_gouraud(self):
        x = np.linspace(-2*np.pi, 2*np.pi, 100)
        t = np.linspace(0, 2*np.pi, 1)

        X, Y, T = np.meshgrid(x, x, t)
        Z = np.sin(X**2+Y**2-T)

        block = amp.blocks.Pcolormesh(
            X[:, :, 0], Y[:, :, 0], Z, t_axis=2, shading="gouraud"
        )
        return amp.Animation([block])

    @animation_compare(baseline_images='Blocks/Imshow', nframes=3)
    def test_Imshow(self):
        x = np.linspace(0, 1, 10)
        X, Y = np.meshgrid(x, x)

        U = []
        for i in range(3):
            U.append(X**2+Y**2+i)

        block = amp.blocks.Imshow(U)
        return amp.Animation([block])

    @animation_compare(baseline_images='Blocks/Quiver', nframes=4)
    def test_Quiver(self):
        x = np.linspace(0, 1, 10)
        X, Y = np.meshgrid(x, x)

        U, V = [], []
        for i in range(4):
            U.append(X**2+Y**2+i)
            V.append(X**2+Y**2+i)

        block = amp.blocks.Quiver(X, Y, U, V)
        return amp.Animation([block])

    @animation_compare(baseline_images='Blocks/Nuke', nframes=3)
    def test_Nuke(self):
        ax = plt.gca()
        sizes = []

        def animate(i):
            sizes.append(i+1)
            ax.set_aspect("equal")
            ax.pie(sizes)
        block = amp.blocks.Nuke(animate, length=3, ax=ax)
        return amp.Animation([block])
