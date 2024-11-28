import numpy as np

def __contourf__(ax, nc_obj, pas, vmin, vmax, **kwargs):
    try:
        if not 'cmap' in kwargs:
            kwargs['cmap'] = 'jet'
    except:
        kwargs['cmap'] = 'jet'
    levels = np.arange(vmin, vmax, pas)
    sc = ax.contourf(nc_obj.lon, nc_obj.lat, nc_obj.data, levels, kwargs=kwargs)
    return ax, sc
