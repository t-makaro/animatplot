Using Jupyter
=============

In order to display interactive animations in jupyter notebook or lab, 
use one of the following line magics:

.. code-block:: python

    %matplotlib notebook  # notebook only
    %matplotlib ipympl  # notebook or lab
    %matplotlib widget  # notebook or lab (equivalent to ipympl)

Or if you prefer matplotlib to display a figure in a native window:

.. code-block:: python

    %matplotlib qt
