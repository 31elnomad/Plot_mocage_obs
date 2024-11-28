def __contourf__(self, ax, nc_obj, **kwargs):
        print(nc_obj.data)
        print('ok')
        cmap = self.config_plot['cmap']
        nlevs = int(self.config_plot['plot_opt'].split(':')[1])
        ax.contourf(nc_obj.lon, nc_obj.lat, nc_obj.data, nlevs, cmap=cmap, **kwargs)
        return ax
