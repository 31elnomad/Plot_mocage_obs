import numpy as np

def __contourf__(ax, nc_obj, pas, vmin, vmax, **kwargs):
    try:
        if not 'cmap' in kwargs:
            kwargs['cmap'] = 'jet'
    except:
        kwargs['cmap'] = 'jet'
    levels = np.arange(vmin, vmax+pas, pas)
    sc = ax.contourf(nc_obj.lon, nc_obj.lat, nc_obj.data, levels, kwargs=kwargs)
    return ax, sc

def __print_colorbar__(fig, sc, config_plot):
    print('ok1')
    colorbar = config_plot['colorbar'].split(':')
    print(colorbar)
    if colorbar[0].lower() not in ['t', 'true']:
        print('ok1_2')
        if colorbar[1].lower() in ['v']:
            fig.subplots_adjust(right=0.8)
            cbar_ax = fig.add_axes([0.84,0.12,0.02, 0.7])
            orientation = 'vertical'
        elif colorbar[1].lower() in ['h']:
            print('ok1_3')
            fig.subplots_adjust(bottom=0.19)
            cbar_ax = fig.add_axes([0.15, 0.12, 0.7, 0.02])
            orientation = 'horizontal'
        cbar = fig.colorbar(sc, 
                        cax=cbar_ax,
                        orientation=orientation,
                        extend=nc_mocage.extend
                        )
    print('ok2')
