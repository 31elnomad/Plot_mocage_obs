import sys
import glob
import os
import datetime
import numpy as np

def create_listfile(config_h5, date):
    if config_h5['type'].lower() in ['h5_sim', 'h5_obs']:
        filename = 'hdf5-std.extract.' + date.strftime('%Y%m%d') + '*'
    elif config_h5['type'].lower() in ['hstat']:
        filename = 'HSTAT+' + date.strftime('%Y%m%d') + '*.h5'
    elif config_h5['type'].lower() in ['hdat']:
        filename = 'HDAT+' + date.strftime('%Y%m%d') + '*.h5'
    dirfile = os.path.join(config_h5['dirin'], filename)
    listfile = glob.glob(dirfile)
    return listfile

def read_h5(config_class, pseudo, date, lonbnd, latbnd, kwargs):
    kwargs = kwargs['kwargs']
    sys.path.append(os.path.abspath(config_class.config['observations']['daimon_path']))
    import daimonobs
    delta = float(config_class.config['observations']['delta'])
    config_h5 = config_class.config[pseudo]
    config_plot = config_class.config[config_class.config['global']['type_plot']]
    # Initialize data and coordinates arrays
    lon = []
    lat = []
    data = []
    d2 = date
    d1 = d2 - datetime.timedelta(hours=1)
    TimeBnd = (d1, d2)
    listfile = create_listfile(config_h5, date)

    for file in listfile:
        if pseudo.lower() in ['iasi_a', 'iasi_b', 'iasi_c']:
            obj = daimonobs.DefInstrument(config_h5['instrname'],
                                          'IasiInstr',
                                          species=kwargs['species'])
            unit = 'DU'
        elif pseudo.lower() in ['iasi_a_lh', 'iasi_b_lh', 'iasi_c_lh']:
            obj = daimonobs.DefInstrument(config_h5['instrname'],
                                          'IasiInstr',
                                          species=kwargs['species'],
                                          nmaxlevs=kwargs['nmaxlevs'])
            unit = 'DU'
        elif pseudo.lower() in ['omi']:
            obj = daimonobs.DefInstrument(config_h5['instrname'],
                                          'OMIInstr',
                                          species=kwargs['species'])
            unit = 'DU'
        elif pseudo.lower() in ['tropomi']:
            obj = daimonobs.DefInstrument(config_h5['instrname'],
                                          'TropomiInstr',
                                          species=kwargs['species'])
            unit = 'DU'
        elif pseudo.lower() in ['tropomi_lh']:
            obj = daimonobs.DefInstrument(config_h5['instrname'],
                                          'TropomiConcInstr',
                                          species=kwargs['species'],
                                          nmaxlevs=kwargs['nmaxlevs'])
            unit = 'DU'
        elif pseudo.lower() in ['viirs']:
            obj = daimonobs.DefInstrument(config_h5['instrname'],
                                          'ViirsAOD',
                                          wv=kwargs['wv'])
        elif pseudo.lower() in ['modis']:
            obj = daimonobs.DefInstrument(config_h5['instrname'],
                                          'MODIS_AOD',
                                          wv=kwargs['wv'])

        # Read data from the current file
        if config_h5['type'].lower() in ['h5_sim', 'HSTAT']:
            obj.Read(file, ReadAssim={'Region': config_h5['domain'], 'ObsType': 'Y'})
        else:
            obj.Read(file)
        # Select data within the specified time bounds
        if lonbnd[0] <= lonbnd[1]:
            obj.Select(TimeBnd=TimeBnd, LonBnd=lonbnd, LatBnd=latbnd)
        else:
            obj_copy = obj
            lonbnd_ = list(lonbnd)
            lonbnd_[1]= 180.
            lonbnd_= tuple(lonbnd)
            obj_copy.Select(TimeBnd=TimeBnd, LonBnd=lonbnd_, LatBnd=latbnd)
            lon, lat, data = __read_h5__(obj_copy, lon, lat, data, kwargs)
            lonbnd_ = list(lonbnd)
            lonbnd_[0] = -180.
            lonbnd_ = tuple(lonbnd_)
            obj.Select(TimeBnd=TimeBnd, LonBnd=lonbnd_, LatBnd=latbnd)
        # Append Lon, Lat, and Data to their respective lists
        lon, lat, data = __read_h5__(obj, lon, lat, data, kwargs)
    # Convert Lon, Lat, and Data lists to NumPy arrays
    lon = np.array(lon)
    if central_longitude == 180.:
        lon += central_longitude
        lon[lon > 180.] = lon[lon > 180.] - 2*central_longitude
    lat = np.array(lat)
    data = np.array(data)
    if config_plot['maskmin'].lower() in ['true', 't']:
        if pseudo.lower() in ['iasi_a_lh', 'iasi_b_lh', 'iasi_c_lh', 'tropomi_lh']:
            if len(data.shape) > 1:
                 raise Exception("Le cas avec plusieurs colonnes n'a pas été codé pour les observations")
        mk = data >= float(config_plot['vmin'])
        lon = lon[mk]
        lat = lat[mk]
        data = data[mk]
    return lon, lat, data

    def __read_h5__(obj, lon, lat, data, kwargs):
      lon.extend(obj.lons)
      lat.extend(obj.lats)
      if pseudo.lower() in ['iasi_a_lh', 'iasi_b_lh', 'iasi_c_lh', 'tropomi_lh']:
          data.extend(obj.col[kwargs['species']])
      elif pseudo.lower() in ['iasi_a', 'iasi_b', 'iasi_c', 'tropomi']:
          data.extend(obj.pcol[kwargs['species']])
      elif pseudo.lower()  in ['modis', 'viirs']:
          data.extend(obj.aod[str(kwargs['wv'])])
      return lon, lat, data

