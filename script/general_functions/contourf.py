def __contourf__(ax, nc_obj, **kwargs):
        try:
            if not 'cmap' in kwargs:
                kwargs['cmap'] = 'jet'
        except:
            kwargs['cmap'] = 'jet'
        nlevs = int(self.config_plot['plot_opt'].split(':')[1])
        ax.contourf(nc_obj.lon, nc_obj.lat, nc_obj.data, nlevs, cmap=cmap, kwargs=kwargs)
        return ax
