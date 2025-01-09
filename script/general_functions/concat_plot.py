import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def __concat_plot__(fig, axs, filenames, type_plot, **kwargs):
    print(filenames)
    central_longitude = 0.
    if 'central_longitude' in kwargs:
        central_longitude = kwargs['central_longitude']
    if type_plot in ['map']:   
        if len(filenames) > 1:
            for ax, filename in zip(axs.flat, filenames):
                img = plt.imread(filename)
                ax.imshow(img, extent=[-180,180,-90,90], transform=ccrs.PlateCarree(central_longitude=central_longitude))
                ax.axis('off')
        else:
            img = plt.imread(filenames[0])
            axs.imshow(img, extent=[0,360,-90,90], transform=ccrs.PlateCarree(central_longitude=central_longitude))
            axs.axis('off')
    return axs
    
