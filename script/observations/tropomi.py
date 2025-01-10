def __main_tropomi__(config_class, pseudo, date, lonbnd, latbnd, **kwargs):
    if config_class[pseudo]['overpass'] == 'T' and config_class[pseudo]['type'] not in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        raise Exception ("Not implemented tropomi.py ligne 3")
    elif config_class[pseudo]['overpass'] == 'T' and config_class[pseudo]['type'] in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        from read_mocage_hdat import read_h5
        raise Exception ("Not implemented tropomi.py ligne 6")
    elif config_class[pseudo]['overpass'] == 'F' and config_class[pseudo]['type'] in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        from read_mocage_hdat import read_h5
        lon, lat, data = read_h5(config_class, pseudo, date, lonbnd, latbnd, kwargs)
    elif config_class[pseudo]['overpass'] == 'F' and config_class[pseudo]['type'] not in ['HDAT', 'HSTAT', 'h5_sim', 'h5_obs']:
        raise Exception ("Not implemented tropomi.py ligne 9")
    return lon, lat, data
  
