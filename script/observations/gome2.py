import h5py
import os
import glob
import numpy as np
import datetime
from functools import reduce

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
        lon, lat, data, unit = process_obs_file(config_class, date, pseudo, lonbnd, latbnd, kwargs)
    return lon, lat, data, unit

def process_obs_file(config_class, date, pseudo, lonbnd, latbnd, kwargs):
    if config_class.config[pseudo]['type'] not in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        dir = config_class.config[pseudo]['dirin']
    elif config_class.config[pseudo]['type'] in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs'] and config_class.config[pseudo]['overpass'] == 'T':
        dir = config_class.config[pseudo]['dirpass']
        Detect_flag = ['0', '1', '2', '3']
    listfile = create_listfile_obs(dir, date, pseudo)
    var = config_class.config[pseudo]['var'].split(':')
    lon, lat, data = openfile(confil_class, listfile, date, lonbnd, latbnd)
    return lon, lat, data, 'DU'
        

def openfile(listfile, var, date, lonbnd, latbnd):
    var = config_class.config[pseudo]['var'].split(':')
    Lon, Lat, Data = [], [], []
    for file in listfile:
        print(file)
        err = 0
        try:
            f = h5py.File(file, 'r')
        except:
            print("Skipping file {}".format(file))
            err = 1
            continue
        if err == 0:
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
                if config_class.config[pseudo]['type'] not in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
                    obs_opts = config_class.config[pseudo]['obs_opts'].split(';')
                    for i in range(len(obs_opts)):
                        if obs_opts[i].split(":")[0] in ['volcano_flag']:
                            Detect_flag = obs_opts[i].split(":")[1][1:-1].split(',')
                            print(Detect_flag)
                            quit()
                    kept_obs = np.array([False]*len(kept_time))
                    """for Detect_flag in detect_flag:
                        # index of accepted obs
                        kept_obs = kept_obs +reduce(
                            np.logical_and,
                            [f['DETAILED_RESULTS/SO2/SO2_Flag'][:] == 0] +
                            [kept_times] +
                            [f['DETAILED_RESULTS/SO2/SO2_Volcano_Flag'][:] == Detect_flag]
                            )"""
            from convert_data import __convert_data__
            data, unit = __convert_data__(file_unit, var[1], data)
            Lon.extend(lon[kept_time])
            Lat.extend(lat[kept_time])
            Data.extend(data[kept_time,2])
    return np.array(Lon), np.array(Lat), np.array(Data)
        
    

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
