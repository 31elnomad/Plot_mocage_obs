import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeLocator, LatitudeLocator, LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt

def _set_cartopy_(obj_plot, nc_obj, ax, ligne, col):
    """
    Set up Cartopy projection and features on a given axis.

    Args:
        ax (matplotlib.axes.Axes): Matplotlib axes object for plotting.
        ligne (int): Line number for plotting grid.
        col (int): Column number for plotting grid.

    Returns:
        matplotlib.axes.Axes: Matplotlib axes object with Cartopy projection and features.
    """
    resol = '50m'
    land_color = '#D3D3D3'
    sea_color = '#D3D3D3'
    if obj_plot.proj[0] == 'PlateCarree':
        central_longitude = float(obj_plot.proj[1])
        mapproj = ccrs.PlateCarree(central_longitude=central_longitude)
    else:
        raise Exception("La projection {} nest pas implémenté".format(obj_plot.proj[0]))
    ax.add_feature(
        cfeature.NaturalEarthFeature(
            'physical',
            'land',
            resol,
            edgecolor='black',
            facecolor=land_color,
            alpha=0.5
        )
    )
    ax.add_feature(
        cfeature.NaturalEarthFeature(
            'physical',
            'ocean',
            resol,
            edgecolor='black',
            facecolor=sea_color,
            alpha=0.5
        )
    )
    ax.coastlines(
        resolution=resol,
        color='black',
        zorder=11,
        linewidth=2
    )
    gl = ax.gridlines(
        crs=mapproj,
        draw_labels=True,
        linewidth=0.5,
        color='k',
        alpha=1,
        linestyle='--',
        zorder=12
    )
    gl.xlocator = LongitudeLocator(nbins=int(float(obj_plot.grid[0])))
    gl.xformatter = LongitudeFormatter(auto_hide=False)
    gl.ylocator = LatitudeLocator(nbins=int(float(obj_plot.grid[1])))
    gl.yformatter = LatitudeFormatter(auto_hide=False) 
    gl.top_labels = False
    gl.left_labels = False
    gl.right_labels = False
    gl.bottom_labels = False
    gl.left_labels = True
    gl.bottom_labels = True
    gl.xlabel_style = {'size': 20, 'color': 'black'}
    gl.ylabel_style = {'size': 20, 'color': 'black'}
    if nc_obj.lonbnd[0] > nc_obj.lonbnd[1]:
        raise Exception ("Cas où lonbnd[0] > lonbnd[1] n'est pas implémenté")
    ax.set_extent([nc_obj.lonbnd[0],
                   nc_obj.lonbnd[1],
                   nc_obj.latbnd[0],
                   nc_obj.latbnd[1]],
                  crs=mapproj)
    return ax
        
          
    
