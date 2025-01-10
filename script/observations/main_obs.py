import importlib
import datetime

class obs_mocage:

    def __init__(self, config_class, pseudo, date, **kwargs): 
        self.pseudo = pseudo[1]
        self.config_obs = config_class.config[self.pseudo]
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
        self.script_name = self.config_obs['python_path_obscript'][:-2]
        

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

    def __main_obs__(self):
        module = importlib.import_module(self.script_name)
        self.create_bnd()
        __main_tropomi__(config_class, pseudo, date, lonbnd, latbnd, **kwargs)
          
