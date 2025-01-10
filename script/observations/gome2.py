import h5py
import os
import glob
import numpy as np
import datetime

def __main_gome2__(config_class, pseudo, date, lonbnd, latbnd, **kwargs):
    if config_class.config[pseudo]['overpass'] == 'T' and config_class[pseudo]['type'] not in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        raise Exception ("Not implemented gome2.py ligne 3")
    elif config_class.config[pseudo]['overpass'] == 'T' and config_class.config[pseudo]['type'] in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        from read_mocage_hdat import read_h5
        raise Exception ("Not implemented gome2.py ligne 6")
    elif config_class.config[pseudo]['overpass'] == 'F' and config_class.config[pseudo]['type'] in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        from read_mocage_hdat import read_h5
        lon, lat, data = read_h5(config_class, pseudo, date, lonbnd, latbnd, kwargs)
    elif config_class.config[pseudo]['overpass'] == 'F' and config_class.config[pseudo]['type'] not in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        lon, lat, data = process_obs_file(config_class, date, pseudo, lonbnd, latbnd, kwargs)
    return lon, lat, data

def process_obs_file(config_class, date, pseudo, lonbnd, latbnd, kwargs):
    if config_class.config[pseudo]['type'] not in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        dir = config_class.config[pseudo]['dirin']
    elif config_class.config[pseudo]['type'] in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs'] and config_class.config[pseudo]['overpass'] == 'T':
        dir = config_class.config[pseudo]['dirpass']
    listfile = create_listfile_obs(dir, date, pseudo)
    var = config_class.config[pseudo]['var'].split(':')
    Lon, Lat, Data = [], [], []
    for file in listfile:
        print(file)
        lon, lat, data = openfile(file, var, date, lonbnd, latbnd)
        Lon.extend(lon)
        Lat.extend(Lat)
        Data.extend(data)

def openfile(file, var, date, lonbnd, latbnd):
    f = h5py.File(file, 'r')
    time = f['GEOLOCATION/Time'][:]
    lon = f['GEOLOCATION/LongitudeCentre'][:]
    lat = f['GEOLOCATION/LatitudeCentre'][:]
    kept_time = create_masktime(date, time)
    if var[0] in ['CloudFraction']:
        file_unit = '1'
        data = f['CLOUD_PROPERTIES/CloudFraction'][:]
    elif var[0] in ['ClouHeight']:
        if var[1].lower() in ['m', 'km']:
            file_unit = 'km'
            data = f['CLOUD_PROPERTIES/CloudTopHeight'][:]
        elif var[1].lower() in ['Pa', 'hPa']:
            file_unit = 'hPa'
            data = f['CLOUD_PROPERTIES/CloudTopPressure'][:]
    elif var[0] in ['CloudType']:
        file_unit = '1'
        data = f['CLOUD_PROPERTIES/CloudType'][:]
    elif var[0] in ['SO2', 'SO_2', 'SO_2_tc', 'SO2_tc']:
        file_unit = 'molec cm-2'
        data = f['DETAILED_RESULTS/SO2/VCDCorrected'][:]
        print(data.shape)
        quit()
        flag1 = f['DETAILED_RESULTS/SO2/SO2_Flag'][:]
        flag2 = f['DETAILED_RESULTS/SO2/SO2_Volcano_Flag'][:]
    from convert_data import __convert_data__
    data, unit = __convert_data__(file_unit, var[1], data)
    return lon[kept_time], lat[kept_time], data[kept_time]
        
    

def create_masktime(date, time):
    date_min = date - datetime.timedelta(hours=1)
    date_max = date
    first_date = datetime.datetime(1950, 1, 1)
    time_since = date_min - first_date
    njour = int(time_since.total_seconds()) // (3600*24)
    hour_min = date_min.strftime('%H')
    hour_max = date_max.strftime('%H')
    kept_time = np.empty(len(time)).astype(bool)
    for t in range(len(time)):
        if time[t][0] == njour:
            tmp = time[t][1]/3600000
            if tmp > int(hour_min) and tmp <= int(hour_max):
                kept_time[t] = True
            else:
                kept_time[t] = False
    return kept_time
          



def create_listfile_obs(dir, date, pseudo):
    if pseudo[-1].lower() == 'a':
      sat = 'A'
    elif pseudo[-1].lower() == 'b':
      sat = 'B'
    elif pseudo[-1].lower() == 'c':
      sat = 'C'
    filename = 'GOME_O3-NO2-NO2Tropo-BrO-SO2-H2O-HCHO_L2_{date}*_METOP{x}*.HDF5'.format(date=date.strftime('%Y%m%d'), x=sat)
    listfile = os.path.join(dir, filename)
    listfile = glob.glob(listfile)
    date = date - datetime.timedelta(days=1)
    filename = 'GOME_O3-NO2-NO2Tropo-BrO-SO2-H2O-HCHO_L2_{date}*_METOP{x}*.HDF5'.format(date=date.strftime('%Y%m%d'), x=sat)
    listfile1 = os.path.join(dir, filename)
    listfile = listfile + glob.glob(listfile1)
    return listfile
