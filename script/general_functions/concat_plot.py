import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def __concat_plot__(fig, axs, filenames, finale_name_plot):
    for ax, filename in zip(axs.flat, filenames):
        img = plt.imread(filename)
        ax.imshow(img, extent=[-180,180,-90,90], transform=ccrs.PlateCarree())
        ax.axis('off')
    plt.tight_layout()
    plt.savefig("test.png")
    plt.close()
    