import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from animatplot.xanim import animated_plot


# Create data set
x = np.linspace(-2, 2, 41)
y = np.linspace(-2, 2, 41)
t = np.linspace(0, 2*np.pi, 30)
X, Y, T = np.meshgrid(x, y, t)
data = np.sin(X*X+Y*Y-T)
da = xr.DataArray(data, coords=[('horizontal position', x),
                                ('vertical position', y),
                                ('time', t)])

# Create animated 2D plot
anim, block, timeline = animated_plot(da)
anim.controls()
anim.save_gif('../xarray_imshow')
plt.show()
