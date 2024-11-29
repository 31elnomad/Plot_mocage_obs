import sys
import glob

class obs_mocage:
  
    def __init__(self, config, pseudo, date, var, **kwargs): 
        sys.path.append(os.path.abspath(config['observations']))
        self.pseudo = pseudo[1]
        self.config_h5 = config[self.pseudo]
        self.date = datetime.datetime(int(date[:4]),
                                      int(date[4:6]),
                                      int(date[6:8]),
                                      int(date[8:10]))
        self.var = var
        self.kwargs = kwargs

    def crete_listfile(self):
        if self.config_h5['type'].lower() in ['h5_sim', 'h5_obs']:
            filename = 'hdf5-std.extract.' + self.date.strftime('%Y%m%d') + '*'
        elif self.config_h5['type'].lower() in ['hstat']:
            filename = 'HSTAT+' + self.date.strftime('%Y%m%d') + '*.h5'
        elif self.config_h5['type'].lower() in ['hdat']:
            filename = 'HDAT+' + self.date.strftime('%Y%m%d') + '*.h5'
        dirfile = os.path.join(self.config_h5['dirin'], filename)
        self.listfile = glob.glob(dirfile)

    def read_h5(self):
        for file in self.listfile:
            if self.pseudo.lower() in ['iasi_a', 'iasi_b', 'iasi_c']:
                obj = daimonobs.DefInstrument(self.config_h5['instrname'],
                                              'IasiInstr',
                                              species=kwargs['species'])
          

