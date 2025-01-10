import h5py
import os
import glob

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
        process_obs_file(config_class, date, pseudo)
    return lon, lat, data

def process_obs_file(config_class, date, pseudo):
    if config_class.config[pseudo]['type'] not in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        dir = config_class.config[pseudo]['dirin']
    elif config_class.config[pseudo]['type'] in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs'] and config_class.config[pseudo]['overpass'] == 'T':
        dir = config_class.config[pseudo]['dirpass']
    listfile = create_listfile_obs(dir, date, pseudo)
    var = config_class.config[pseudo]['var'].split(':')
    for file in listfile:
        print(file)
        openfile(file, var)

def openfile(file, var):
    f = h5py.File(file, 'r')
    time = f['GEOLOCATION/Time'][:]
    lon_a = f['GEOLOCATION/LongitudeA'][:]
    lon_b = f['GEOLOCATION/LongitudeB'][:]
    lon_c = f['GEOLOCATION/LongitudeC'][:]
    lon_d = f['GEOLOCATION/LongitudeD'][:]
    lat_a = f['GEOLOCATION/LatitudeA'][:]
    lat_b = f['GEOLOCATION/LatitudeB'][:]
    lat_c = f['GEOLOCATION/LatitudeC'][:]
    lat_d = f['GEOLOCATION/LatitudeD'][:]
    if var[0] in ['CloudFraction']:
        data = f['CLOUD_PROPERTIES/CloudFraction'][:]
    elif var[0] in ['ClouHeight']:
        if var[1].lower() in ['m', 'km']:
            data = f['CLOUD_PROPERTIES/CloudTopHeight'][:]
        elif var[1].lower() in ['Pa', 'hPa']:
            data = f['CLOUD_PROPERTIES/CloudTopPressure'][:]
    elif var[0] in ['CloudType']:
        data = f['CLOUD_PROPERTIES/CloudType'][:]
    elif var[0] in ['SO2', 'SO_2', 'SO_2_tc', 'SO2_tc']:
        data = f['DETAILLED_RESULTS/SO2/VCDCorrected'][:]
        flag1 = f['DETAILLED_RESULTS/SO2/SO2_Flag'][:]
        flag = f['DETAILLED_RESULTS/SO2/SO2_Volcano_Flag'][:]
        
            
    print(flag1)
    quit()



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
    return listfile
