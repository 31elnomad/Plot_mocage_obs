import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplolib.ticker import LongitudeLocator, LatitudeLocator
import matplotlib.pyplot as plt
import numpy as np

def _set_cartopy_(obj_plot, nc_obj, ax, col, ligne, idx):
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
    if obj_plot.proj == 'PlateCarree':
        central_longitude = float(obj_plot.central_longitude)
        mapproj = ccrs.PlateCarree(central_longitude=central_longitude)
    else:
        raise Exception("La projection {} nest pas implémenté".format(obj_plot.proj))
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
        draw_labels=False,
        linewidth=0.5,
        color='k',
        alpha=1,
        linestyle='--',
        zorder=12
    )
    gl.top_labels = False
    gl.right_labels = False
    gl.bottom_labels = False
    gl.left_labels = False
    gl.ylocator = LatitudeLocator(interval=int(float(obj_plot.grid[1])))
    gl.xlocator = LongitudeLocator(interval=int(float(obj_plot.grid[0])))

    if idx % obj_plot.ncol == 0:
        lat_lab = np.arange(-90, 90, int(obj_plot.grid[1]))
        ax.set_yticks(lat_lab)
        ax.yaxis.set_major_formatter(LatitudeFormatter())
        for label in ax.yaxis.get_ticklabels():
            label.set_fontsize(20)
    if obj_plot.ncol * obj_plot.nligne - idx <= obj_plot.ncol:
        lon_lab = np.arange(-180, 180, int(obj_plot.grid[0]))
        lon_lab = lon_lab + float(obj_plot.central_longitude)
        lon_lab[lon_lab>180.] = lon_lab[lon_lab>180.] - 360.
        ax.set_xticks(lon_lab)
        ax.xaxis.set_major_formatter(LongitudeFormatter())
        for label in ax.xaxis.get_ticklabels():
            label.set_fontsize(20)
    if nc_obj.lonbnd[0] > nc_obj.lonbnd[1]:
        raise Exception ("Cas où lonbnd[0] > lonbnd[1] n'est pas implémenté")
    ax.set_extent([nc_obj.lonbnd[0],
                   nc_obj.lonbnd[1],
                   nc_obj.latbnd[0],
                   nc_obj.latbnd[1]],
                  crs=mapproj)
    return ax
        
          
    
