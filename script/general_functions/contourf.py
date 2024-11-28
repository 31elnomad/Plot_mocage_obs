def __contourf__(ax, nc_obj, nlevs, **kwargs):
        try:
            if not 'cmap' in kwargs:
                kwargs['cmap'] = 'jet'
        except:
            kwargs['cmap'] = 'jet'
        ax.contourf(nc_obj.lon, nc_obj.lat, nc_obj.data, nlevs, kwargs=kwargs)
        return ax
