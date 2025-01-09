import sys
import glob
import os
import datetime
import numpy as np

class obs_mocage:
  
    def __init__(self, config_class, pseudo, date, **kwargs): 
        sys.path.append(os.path.abspath(config_class.config['observations']['daimon_path']))
        self.pseudo = pseudo[1]
        self.config_h5 = config_class.config[self.pseudo]
        self.date = datetime.datetime(int(date[:4]),
                                      int(date[4:6]),
                                      int(date[6:8]),
                                      int(date[8:10]))
        self.config_plot = config_class.config[config_class.config['global']['type_plot']]
        self.kwargs = kwargs
        self.delta = float(config_class.config['observations']['delta'])
        self.central_longitude = 0.
        if 'central_longitude' in kwargs:
            self.central_longitude = kwargs['central_longitude']

    def create_listfile(self):
        if self.config_h5['type'].lower() in ['h5_sim', 'h5_obs']:
            filename = 'hdf5-std.extract.' + self.date.strftime('%Y%m%d') + '*'
        elif self.config_h5['type'].lower() in ['hstat']:
            filename = 'HSTAT+' + self.date.strftime('%Y%m%d') + '*.h5'
        elif self.config_h5['type'].lower() in ['hdat']:
            filename = 'HDAT+' + self.date.strftime('%Y%m%d') + '*.h5'
        dirfile = os.path.join(self.config_h5['dirin'], filename)
        self.listfile = glob.glob(dirfile)

    def create_bnd(self):
        bnd = self.config_plot['boundary'].split('/')
        tmp = bnd[0].split(',')
        if bnd[0] == 'None':
            self.lonbnd = (-180., 180.)
        elif len(tmp) == 1 or float(tmp[0]) == float(tmp[1]) == 0:
            self.lonbnd = (float(tmp[0])-self.delta/2, float(tmp[0])+self.delta/2)
        else:
            self.lonbnd = (float(tmp[0]), float(tmp[1]))
        tmp = bnd[1].split(',')
        if bnd[0] == 'None':
            self.latbnd = (-180., 180.)
        elif len(tmp) == 1 or float(tmp[0]) == float(tmp[1]) == 0:
            self.latbnd = (float(tmp[0])-self.delta/2, float(tmp[0])+self.delta/2)
        else:
            self.latbnd = (float(tmp[0]), float(tmp[1]))

    def read_h5(self):
        import daimonobs
        # Initialize data and coordinates arrays
        self.lon = []
        self.lat = []
        self.data = []
        d2 = self.date
        d1 = d2 - datetime.timedelta(hours=1)
        TimeBnd = (d1, d2)
        self.create_listfile()
        self.create_bnd()
        for file in self.listfile:
            if self.pseudo.lower() in ['iasi_a', 'iasi_b', 'iasi_c']:
                obj = daimonobs.DefInstrument(self.config_h5['instrname'],
                                              'IasiInstr',
                                              species=self.kwargs['species'])
                self.unit = 'DU'
            elif self.pseudo.lower() in ['iasi_a_lh', 'iasi_b_lh', 'iasi_c_lh']:
                obj = daimonobs.DefInstrument(self.config_h5['instrname'],
                                              'IasiInstr',
                                              species=self.kwargs['species'],
                                              nmaxlevs=self.kwargs['nmaxlevs'])
                self.unit = 'DU'
            elif self.pseudo.lower() in ['omi']:
                obj = daimonobs.DefInstrument(self.config_h5['instrname'],
                                              'OMIInstr',
                                              species=self.kwargs['species'])
                self.unit = 'DU'
            elif self.pseudo.lower() in ['tropomi']:
                obj = daimonobs.DefInstrument(self.config_h5['instrname'],
                                              'TropomiInstr',
                                              species=self.kwargs['species'])
                self.unit = 'DU'
            elif self.pseudo.lower() in ['tropomi_lh']:
                obj = daimonobs.DefInstrument(self.config_h5['instrname'],
                                              'TropomiConcInstr',
                                              species=self.kwargs['species'],
                                              nmaxlevs=self.kwargs['nmaxlevs'])
                self.unit = 'DU'
            elif self.pseudo.lower() in ['viirs']:
                obj = daimonobs.DefInstrument(self.config_h5['instrname'],
                                              'ViirsAOD',
                                              wv=self.kwargs['wv'])
            elif self.pseudo.lower() in ['modis']:
                obj = daimonobs.DefInstrument(self.config_h5['instrname'],
                                              'MODIS_AOD',
                                              wv=self.kwargs['wv'])

            # Read data from the current file
            if self.config_h5['type'].lower() in ['h5_sim', 'HSTAT']:
                obj.Read(file, ReadAssim={'Region': self.config_h5['domain'], 'ObsType': 'Y'})
            else:
                obj.Read(file)
            # Select data within the specified time bounds
            if self.lonbnd[0] <= self.lonbnd[1]:
                obj.Select(TimeBnd=TimeBnd, LonBnd=self.lonbnd, LatBnd=self.latbnd)
            else:
                import copy
                obj_copy = obj
                lonbnd = list(self.lonbnd)
                lonbnd[1]= 180.
                lonbnd = tuple(lonbnd)
                obj_copy.Select(TimeBnd=TimeBnd, LonBnd=lonbnd, LatBnd=self.latbnd)
                self.__read_h5__(obj_copy)
                lonbnd = list(self.lonbnd)
                lonbnd[0] = -180.
                lonbnd = tuple(lonbnd)
                obj.Select(TimeBnd=TimeBnd, LonBnd=lonbnd, LatBnd=self.latbnd)
            # Append Lon, Lat, and Data to their respective lists
            self.__read_h5__(obj)
        # Convert Lon, Lat, and Data lists to NumPy arrays
        self.lon = np.array(self.lon)
        if self.central_longitude == 180.:
            self.lon[self.lon + self.central_longitude > 180.] -= self.central_longitude
            self.lon[self.lon + self.central_longitude <= 180.] += self.central_longitude
        self.lat = np.array(self.lat)
        self.data = np.array(self.data)
        if self.config_plot['maskmin'].lower() in ['true', 't']:
            if self.pseudo.lower() in ['iasi_a_lh', 'iasi_b_lh', 'iasi_c_lh', 'tropomi_lh']:
                if len(self.data.shape) > 1:
                    raise Exception("Le cas avec plusieurs colonnes n'a pas été codé pour les observations")
            mk = self.data >= float(self.config_plot['vmin'])
            self.lon = self.lon[mk]
            self.lat = self.lat[mk]
            self.data = self.data[mk]

    def __read_h5__(self, obj):
      self.lon.extend(obj.lons)
      if len(self.lon) > 0:
          print(self.lon)
          quit()
      self.lat.extend(obj.lats)
      if self.pseudo.lower() in ['iasi_a_lh', 'iasi_b_lh', 'iasi_c_lh', 'tropomi_lh']:
          self.data.extend(obj.col[self.kwargs['species']])
      elif self.pseudo.lower() in ['iasi_a', 'iasi_b', 'iasi_c', 'tropomi']:
          self.data.extend(obj.pcol[self.kwargs['species']])
      elif self.pseudo.lower()  in ['modis', 'viirs']:
          self.data.extend(obj.aod[str(self.kwargs['wv'])])
      

