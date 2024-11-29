import numpy as np

def __contourf__(ax, nc_obj, pas, vmin, vmax, **kwargs):
    if not 'cmap' in kwargs:
        kwargs['cmap'] = 'jet'
    levels = np.arange(vmin, vmax+pas, pas)
    sc = ax.contourf(nc_obj.lon,
                     nc_obj.lat,
                     nc_obj.data,
                     levels,
                     kwargs=kwargs)
    return ax, sc
    
def __scatter__(ax, nc_obj, markersize, vmin, vmax, **kwargs):
    if not 'cmap' in kwargs:
        kwargs['cmap'] = 'jet'
    if len(nc_obj.data.shape) == 2:
        mapx, mapy = __gridmap__(nc_obj)
        sc = ax.scatter(
            mapx,
            mapy,
            s=float(markersize),
            c=nc_obj.data,
            marker='s',
            zorder=10,
            vmin=vmin,
            vmax=vmax,
            alpha=1.,
            **kwargs)
    return ax, sc
        
def __gridmap__(nc_obj):
    if nc_obj.lonbnd[0] != nc_obj.lonbnd[1] and nc_obj.latbnd[0] != nc_obj.latbnd[1]:
        mapx = np.repeat(nc_obj.lon.reshape(1, -1), nc_obj.lat.shape[0], axis=0)
        mapy = np.repeat(nc_obj.lat.reshape(-1, 1), nc_obj.lon.shape[0], axis=1)
    else:
        raise Exception("__gridmap__ n'est pas codé pour ce cas")
    return mapx, mapy

def __print_colorbar__(fig, sc, config_plot, obj_data, unit, var):
    colorbar = config_plot['colorbar'].split(':')
    if colorbar[0].lower() in ['t', 'true']:
        if colorbar[1].lower() in ['v']:
            fig.subplots_adjust(right=0.8)
            cbar_ax = fig.add_axes([0.84,0.12,0.02, 0.7])
            orientation = 'vertical'
        elif colorbar[1].lower() in ['h']:
            fig.subplots_adjust(bottom=0.19)
            cbar_ax = fig.add_axes([0.15, 0.12, 0.7, 0.02])
            orientation = 'horizontal'
        cbar = fig.colorbar(sc, 
                        cax=cbar_ax,
                        orientation=orientation,
                        extend=obj_data.extend
                        )
        if unit is not None:
            cbar.set_label("{} ({})".format(var, unit), fontsize=20)
        else:
            cbar.set_label("{}".format(var), fontsize=20)
        cbar.ax.tick_params(labelsize=20)
    return cbar
