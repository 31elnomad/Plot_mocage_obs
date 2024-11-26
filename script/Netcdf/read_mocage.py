#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""

import os
import sys
import datetime
import xarray as xr

class Netcdf_mocage:

    def __init__(self, config_class, pseudo, date, var):
        self.pseudo = pseudo[1]
        self.config_nc = config_class.config[self.pseudo]
        self.date = datetime.datetime(int(date[:4]),
                                      int(date[4:6]),
                                      int(date[6:8]),
                                      int(date[8:10])) # 2024010100
        self.var = var #SO_2_tc:DU,SO_2:1e9
        self.domain = self.config_nc['domain']
        self.user = self.config_nc['user']
        self.tree = self.config_nc['tree']
        self.type_file = self.config_nc['type_file']
        if self.tree not in ['script']:
            self.conf = self.config_nc['conf']
            self.nameexp = self.config_nc['nameexp']
            self.suffix = self.config_nc['suffix']
            self.group = self.config_nc['group']
            self.echeance = int(self.config_nc['echeance'])
        elif self.tree in ['script']:
            self.type_exp = self.config_nc['typeexp'].lower()
            self.wlength = None
            if self.type_exp.lower() not in ['direct']:
                self.wlength = int(self.config_nc['wlength'])       

    def create_filename(self):
        self.dirhost = f'/home/{self.user}/MOCAGEHM/{self.nameexp}/'
        self.filename2, self.filename3, self.filename4 = None, None, None
        
        if self.type_exp.lower() in ['direct']:
            self.filename1 = f'HM{self.domain.upper()} + {self.date.strftime('%Y%m%d%H')}.nc'
        elif self.type_exp.upper() in ['ANA', 'DRY', 'BKG']:
            nwind, nwind1 = compyte_nwind(self.wlength, int(self.date.hour))
            filename = f'HM{self.domain.upper()}+{self.date.strftime("%Y%m%d%H")}'
            w_exp = f'+{self.type_exp.upper()}"_W{str(nwind).zfill(2)}.nc'
            self.filename1 = filename + w_exp
            if self.wlength != 1:
                w_exp = f'+{self.type_exp.upper()}"_W{str(nwind1).zfill(2)}.nc'
                self.filename2 = filename + w_exp
            if self.type_exp.upper() == 'ANA':
                self.filename3 = filename + f'+BKG_W{str(nwind).zfill(2)}.nc'
                self.filename4 = filename + f'+BKG_W{str(nwind1).zfill(2)}.nc'
        else:
            raise Exception('{} is not implemented'.format(self.type_exp))


    def getfile(self, config_class):
        HOST = self.config_nc['host']
        self.dirtmp = None
        if self.config_nc['getfile'].lower() in ['t', 'true']:
            return_dataset = False
            out_file_name = "{exp}_{dom}_{dt}00-{hhh}.{ext}"
            self.dirtmp = config_class.config['global']['dirtmp'].split('/')
            self.dirtmp.append(self.pseudo)
            if self.tree in ['vortex']:
                self.outfile_name = outfile_name.format(
                        exp=self.nameexp,
                        dom=self.domain.lower(),
                        dt=self.date.strftime('%Y%m%d'),
                        hhh=str(int(self.date.strftime('%H')) + self.echeance).zfill(3),
                        ext='netcdf')
                if self.group in ['analyse']:
                    self.dirtmp.append('A')
                else:
                    self.dirtmp.append('P')
            elif self.tree in ['script']:
                self.outfile_name = outfile_name.format(
                        exp=self.pseudo,
                        dom=self.domain.lower(),
                        dt=self.date.strftime('%Y%m%d'),
                        hhh=str(int(self.date.strftime('%H')) + self.echeance).zfill(3),
                        ext='netcdf')
            self.dirtmp = '/' +  os.path.join(*self.dirtmp)   
            if not os.path.isdir(self.dirtmp):
                os.makedirs(self.dirtmp)
        if self.tree.lower() in ['vortex', 'oper', 'dble', 'mirr']:  
            if self.type_file in ['daily', 'min', 'max', 'hourly', 'post_cams', 'post_prevair']:
                self.post_process = self.type_file
            else:
                self.post_process = False
            
            if self.config_nc['getfile'].lower() in ['t', 'true']:
                if not os.path.exists(os.path.join(self.dirtmp, out_filename)):
                    out_file = self.__get_file__(False, HOST, [self.var[0]])
                else:
                    ds = xr.open_dataset(outfile_name)
                    pres_var = list(ds.keys())
                    if self.var[0] not in pres_var:
                        pres_var.append(self.var[0])
                        out_file = self.__get_file__(False, HOST, pres_var)
                    else:
                        print('File {} already contains {}'.format(outfile_name, self.var[0]))
            else:
                 out_file = self.__get_file__(True, HOST, 'all')    
        elif self.tree.lower() in ['script', 'scripts']:
            self.create_filename()
            err = 1
            for filename in [self.filename1, self.filename2, self.filename3, self.filename4]:
                if err == 1:
                    try:
                        if self.config_nc['getfile'].lower() in ['t', 'true']:
                            if not os.path.exists(os.path.join(self.dirtmp, self.out_filename)):
                                out_file = self.__get_file__(False, HOST, [self.var[0]])
                            else:
                                ds = xr.open_dataset(os.path.join(self.dirtmp, self.out_filename))
                                pres_var = list(ds.keys())
                                if self.var[0] not in pres_var:
                                    pres_var.append(self.var[0])
                                    os.remove(os.path.join(self.dirtmp, self.outfile_name))
                                    out_file = self.__get_file__(False, HOST, pres_var)
                                else:
                                    print('File {} already contains {}'.format(self.outfile_name, self.var[0]))
                        else:
                             out_file = __get_file__(self, True, HOST, 'all') 
                        err = 0
                    except:
                        pass
            if err == 1:
                raise Exception("Aucun fichier 'script' n'a été trouvé")
        else:
            raise Exception("{} est inconnu ou non implémenté".format(self.tree))
            
            
    def __get_file__(self, return_dataset, HOST, listvar, **kwargs):
        if self.tree in ['vortex']:
            from get_data import get_mocage
            if return_dataset is False:
                self.dirtmp = './'
            out_file = get_mocage(exp=self.nameexp,
                                  vconf=self.conf,
                                  date=self.date,
                                  domain=self.domain.lower(),
                                  term=self.echeance+int(self.date.strftime('%H')),
                                  cutoff=self.suffix,
                                  output_dir=self.dirtmp,
                                  post_process=self.post_process,
                                  kept_vars=listvar,
                                  vortex_dir=self.group,
                                  ext='netcdf',
                                  return_dataset=return_dataset,
                                  host=HOST,
                                  user=self.user) 
            print(out_file)
        else:
            try:
                remote_file = os.path.join(self.dirhost, kwargs['filename'])
            except:
                raise Exception("kwargs['filename'] doit être défini") 
            from get_data import get_login_info, ftp_get_buffer
            login_info = get_login_info(HOST)
            r = ftp_get_buffer(remote_file, HOST, login_info)
            if return_dataset is True:
                ds = xr.load_dataset(r)
                r.close()
            else:
                out_file = os.path.join(self.dirtmp, self.out_file_name)
                ds = xr.open_dataset(r)
                ds = ds[kept_vars]
                ds.to_netcdf(
                    out_file,
                    encoding={var: {"zlib": True} for var in kept_vars},
                )
                r.close()
                ds = None
            
        return ds
        
        

    def process_netcdf(self, config_class):
        if self.tree.lower() in ['vortex', 'oper', 'dble', 'mirr']:  
            out_file = self.getfile(config_class)
            print(out_file)
        """self.create_filename()
        if config_class.config[self.pseudo]['get_file'].upper() in ['TRUE', 'T']:
            self.getfile(config_class)
        else:
            raise Exception("le cas get_file is False n'est pas implémenté")"""
            
        
                
                                   
        
                        

def compute_nwind(wlength, hour):
    if hour == 0:
        nwind = 1
        nwind1 = nwind
    else:
        if wlength == 1:
            nwind = hour
            nwind1 = nwind
        else:
            nwind = hour // wlength + 1
            nwind1 = hour // wlength
    return nwind, nwind1

                             
        
        
                             
                                     
        
        
