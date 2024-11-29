import numpy as np

def process_res(results):
    sc = None
    obj_data = None
    var = None
    filenames = []
    unit = None
    for r in results:
        filenames.append(r[0])
        if sc is None and r[1] is not None:
            sc = r[1]
        if obj_data is None and r[2] is not None:
            obj_data = r[2]
        if var is None and r[3] is not None:
            var = r[3]
            unit = r[4]
    if var is not None:
        var = var[0]
    return filenames, sc, obj_data, var, unit

def add_plot(ax, col, ligne, order, var, date, pseudo, xlim, ylim, config_plot, **kwargs):
    if order[0] == 'exp':
        title = pseudo[1]
    if order[1] == 'date':
        txt = date
    if ligne == 0:
        ax.set_title(title, fontsize=20)
    loc_h = ylim[1] - 0.2*abs(ylim[1]-ylim[0])
    loc = xlim[1] - 0.8*abs(xlim[1]-xlim[0])
    if col == 0:
        ax.text(loc, loc_h, txt, fontsize=16, color='white', bbox=dict(facecolor='black'), fontweight='bold')
    if 'add' in list(config_plot.keys()):
        if config_plot['add'] != 'None':
            listvolc = config_plot['add'].split(',')
            for volc in listvolc:
                print ("Ajout d'un triangle pour le volcan {}".format(volc.lower()))
                filename = 'database/volcanoes.csv'
                lon, lat = read_csv(filename, volc.lower())
                ax.plot(lon, lat,
                        "^",
                        markersize=30,
                        color='black')

def read_csv(filename, name):
    import pandas as pd
    df = pd.read_csv(filename, sep = ';')
    tmp = df[df['name'] == name]
    lon = np.array(tmp['longitude'])
    lat = np.array(tmp['latitude'])
    return lon, lat


            
        
