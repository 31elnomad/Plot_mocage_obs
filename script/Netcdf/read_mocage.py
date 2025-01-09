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
import numpy as np

class Netcdf_mocage:

    def __init__(self, config_class, pseudo, date, var, **kwargs):
        self.plot = config_class.config['global']['type_plot']
        self.config_plot = config_class.config[self.plot]
        if pseudo is None:
            self.pseudo = None
        else:
            self.pseudo = pseudo[1]
        if self.pseudo is not None:
            self.config_nc = config_class.config[self.pseudo]
        else:
            self.config_nc = None
        if date is None:
            self.date = None
        else:
            self.date = datetime.datetime(int(date[:4]),
                                          int(date[4:6]),
                                          int(date[6:8]),
                                          int(date[8:10])) # 2024010100
        if var is None:
            self.var = None
        else:
            self.var = var #SO_2_tc:DU,SO_2:1e9
        if self.config_nc is not None:
            self.domain = self.config_nc['domain']
            self.user = self.config_nc['user']
            self.tree = self.config_nc['tree']
            self.type_file = self.config_nc['type_file']
            self.plot_type = config_class.config['global']['type_plot']
            self.nameexp = self.config_nc['nameexp']
            if self.tree not in ['script']:
                self.conf = self.config_nc['conf']
                self.suffix = self.config_nc['suffix']
                self.group = self.config_nc['group']
                self.echeance = int(self.config_nc['echeance'])
            elif self.tree in ['script']:
                self.type_exp = self.config_nc['typeexp'].lower()
                self.wlength = None
                self.echeance = 0
                if self.type_exp.lower() not in ['direct']:
                    self.wlength = int(self.config_nc['wlength']) 
            if self.plot in ['map']:
                if 'central_longitude' in kwargs:
                    self.central_longitude = kwargs['central_longitude']
                else:
                    raise Exception("Central longitude na pas été trouvé dans la class Netcdf")
            else:
                self.central_longitude = 0.
                if 'central_longitude' in kwargs:
                    self.central_longitude = kwargs['central_longitude']
                

    def create_filename(self):
        self.dirhost = f'/home/{self.user}/MOCAGEHM/{self.nameexp}/'
        self.filename2, self.filename3, self.filename4 = None, None, None
        
        if self.type_exp.lower() in ['direct']:
            self.filename1 = f'HM{self.domain.upper()} + {self.date.strftime('%Y%m%d%H')}.nc'
        elif self.type_exp.upper() in ['ANA', 'DRY', 'BKG']:
            nwind, nwind1 = compute_nwind(self.wlength, int(self.date.hour))
            filename = f'HM{self.domain.upper()}+{self.date.strftime("%Y%m%d%H")}'
            w_exp = f'+{self.type_exp.upper()}_W{str(nwind).zfill(2)}.nc'
            self.filename1 = filename + w_exp
            if self.wlength != 1:
                w_exp = f'+{self.type_exp.upper()}_W{str(nwind1).zfill(2)}.nc'
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
                self.outfile_name = out_file_name.format(
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
                self.outfile_name = out_file_name.format(
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
                if not os.path.exists(os.path.join(self.dirtmp, self.outfile_name)):
                    ds = self.__get_file__(False, HOST, [self.var[0], 'a_hybr_coord', 'b_hybr_coord', 'air_pressure_at_surface'])
                else:
                    ds = xr.open_dataset(os.path.join(self.dirtmp, self.outfile_name))
                    pres_var = list(ds.keys())
                    if self.var[0] not in pres_var:
                        pres_var.append(self.var[0])
                        if 'a_hybr_coord' not in pres_var:
                            pres_var.append('a_hybr_coord')
                        if 'b_hybr_coord' not in pres_var:    
                            pres_var.append('b_hybr_coord')
                        if 'air_pressure_at_surface' not in pres_var:
                            pres_var.append('air_pressure_at_surface')
                        os.remove(os.path.join(self.dirtmp, self.outfile_name))
                        ds = self.__get_file__(False, HOST, pres_var)
                    else:
                        print('File {} already contains {}'.format(self.outfile_name, self.var[0]))
            else:
                 ds = self.__get_file__(True, HOST, 'all')    
        elif self.tree.lower() in ['script', 'scripts']:
            self.create_filename()
            err = 1
            for filename in [self.filename1, self.filename2, self.filename3, self.filename4]:
                if err == 1:
                    self.out_filename = filename
                    a=1
                    if a == 1:
                        if self.config_nc['getfile'].lower() in ['t', 'true']:
                            if not os.path.exists(os.path.join(self.dirtmp, self.out_filename)):
                                ds = self.__get_file__(False,
                                                       HOST,
                                                       [self.var[0], 'a_hybr_coord', 'b_hybr_coord', 'air_pressure_at_surface'],
                                                       filename=self.out_filename)
                            else:
                                ds = xr.open_dataset(os.path.join(self.dirtmp, self.out_filename))
                                pres_var = list(ds.keys())
                                if self.var[0] not in pres_var:
                                    pres_var.append(self.var[0])
                                    if 'a_hybr_coord' not in pres_var:
                                        pres_var.append('a_hybr_coord')
                                    if 'b_hybr_coord' not in pres_var:    
                                        pres_var.append('b_hybr_coord')
                                    if 'air_pressure_at_surface' not in pres_var:
                                        pres_var.append('air_pressure_at_surface')
                                    os.remove(os.path.join(self.dirtmp, self.outfile_name))
                                    ds = self.__get_file__(False, HOST, pres_var)
                                else:
                                    print('File {} already contains {}'.format(self.outfile_name, self.var[0]))
                        else:
                             ds = self.__get_file__(True, HOST, 'all', filename=self.out_filename) 
                        err = 0
                    #except:
                    #    pass
            if err == 1:
                raise Exception("Aucun fichier 'script' n'a été trouvé")
        else:
            raise Exception("{} est inconnu ou non implémenté".format(self.tree))
        return ds
            
    def __get_file__(self, return_dataset, HOST, listvar, **kwargs):
        if self.tree in ['vortex']:
            from get_data import get_mocage
            if return_dataset is True:
                self.dirtmp = './'
            ds = get_mocage(exp=self.nameexp,
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
            if return_dataset is False:
                ds = None
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
                out_file = os.path.join(self.dirtmp, kwargs['filename'])
                ds = xr.open_dataset(r)
                ds = ds[listvar]
                ds.to_netcdf(
                    out_file,
                    encoding={var: {"zlib": True} for var in listvar},
                )
                r.close()
                ds = None
        return ds

    def cmp_boundaries(self, config_class):
        plot = config_class.config['global']['type_plot']
        self.boundary = config_class.config[plot]['boundary'].split('/')
        if self.boundary[0] != 'None':
            if len(self.boundary[0].split(',')) == 1:
                tmp = self.boundary[0].split(',')
                tmp = [float(i) for i in tmp]
                if tmp[0] >= self.lonbnd[0] and tmp[0] <= self.lonbnd[1]:
                    self.lonbnd = [tmp[0], tmp[0]]
                else:
                    raise Exception("La longitude donnée dans [plot][boundary] est en dehors du domain {}".format(self.domain.lower()))
            elif len(self.boundary[0].split(',')) == 2:
                tmp = self.boundary[0].split(',')
                tmp = [float(i) for i in tmp]
                if tmp[0] >= self.lonbnd[0] and tmp[0] <= self.lonbnd[1] and tmp[1] >= self.lonbnd[0] and tmp[1] <= self.lonbnd[1]:
                    if abs(tmp[1]-self.central_longitude) <= 180:
                        self.lonbnd = [tmp[0]-self.central_longitude, abs(tmp[1]-self.central_longitude)]
                    else:
                        self.lonbnd = [tmp[0]-self.central_longitude, tmp[1]+self.central_longitude]
                else:
                    raise Exception("Les longitudes données dans [plot][boundary] sont en dehors du domain {}".format(self.domain.lower()))
            else:
                raise Exception('Probleme, il y a 3 longitudes données dans boundary')
        if self.boundary[1] != 'None':
            if len(self.boundary[1].split(',')) == 1:
                tmp = self.boundary[1].split(',')
                tmp = [float(i) for i in tmp]
                if tmp[0] >= self.latbnd[0] and tmp[0] <= self.latbnd[1]:
                    self.latbnd = [tmp[0], tmp[0]]
                else:
                    raise Exception("La latitude donnée dans [plot][boundary] est en dehors du domain {}".format(self.domain.lower()))
            elif len(self.boundary[1].split(',')) == 2:
                tmp = self.boundary[1].split(',')
                tmp = [float(i) for i in tmp]
                if tmp[0] >= self.latbnd[0] and tmp[0] <= self.latbnd[1] and tmp[1] >= tmp[0] and tmp[1] >= self.latbnd[0] and tmp[1] <= self.latbnd[1]:
                    self.latbnd = [tmp[0], tmp[1]]
                else:
                    raise Exception("Les latitudes données dans [plot][boundary] sont en dehors du domain {}".format(self.domain.lower()))
            else:
                raise Exception('Probleme, il y a 3 latitudes données dans boundary')
        if self.boundary[2] != 'None':
            if len(self.boundary[2].split(',')) == 1:
                tmp = self.boundary[2].split(',')
                tmp = [int(i) for i in tmp]
                if tmp[0] >= self.levbnd[0] and tmp[0] <= self.levbnd[1]:
                    self.levbnd = [tmp[0], tmp[0]]
                else:
                    raise Exception("Le level donnée dans [plot][boundary] est en dehors du domain {}".format(self.domain.lower()))
            elif len(self.boundary[2].split(',')) == 2:
                tmp = self.boundary[2].split(',')
                tmp = [int(i) for i in tmp]
                if tmp[0] >= self.levbnd[0] and tmp[0] <= self.levbnd[1] and tmp[1] >= tmp[0] and tmp[1] >= self.levbnd[0] and tmp[1] <= self.levbnd[1]:
                    self.levbnd = [tmp[0], tmp[1]]
                else:
                    raise Exception("Les levels données dans [plot][boundary] sont en dehors du domain {}".format(self.domain.lower()))
            else:
                raise Exception('Probleme, il y a 3 levels données dans boundary')

    def selectdata(self, ds):
        self.lon = ds['lon'].values
        self.lat = ds['lat'].values
        self.lev = ds['lev'].values
        self.data = ds[self.var[0]].squeeze().values
        dim = len(self.data.shape)
        self.psurf = ds['air_pressure_at_surface'].squeeze().values
        self.a = ds['a_hybr_coord'].values
        self.b = ds['b_hybr_coord'].values
        tmp = list(np.abs(self.lon - (self.lonbnd[0] + self.central_longitude)))
        idx_lon1 = np.argmin(tmp)
        tmp = list(np.abs(self.lat - self.latbnd[0]))
        idx_lat1 = np.argmin(tmp)
        tmp = list(np.abs(self.lev - self.levbnd[0]))
        idx_lev1 = np.argmin(tmp)
        
        if self.lonbnd[0] != self.lonbnd[1]:
            if abs(self.lonbnd[1] + self.central_longitude) <= 180.:
                tmp = list(np.abs(self.lon - (self.lonbnd[1] + self.central_longitude)))
            else:
                tmp = list(np.abs(self.lon - (self.lonbnd[1] - self.central_longitude)))
            idx_lon2 = np.argmin(tmp)
            mask = np.empty_like(self.lon).astype(bool)
            mask[:] = False
            if idx_lon1 < idx_lon2:
                mask[idx_lon1:idx_lon2]  = True
            else:
                mask[idx_lon1:] = True
                mask[:idx_lon2] = True
            print(mask)
            quit()
            self.lon = self.lon[mask]
            if len(self.data.shape) == 3:
                self.data = self.data[:, :, mask]
            else:
                self.data = self.data[:, mask]
            self.psurf = self.psurf[:, mask]
        else:
            self.lon = self.lon[idx_lon1]
            if len(self.data.shape) == 3:
                self.data = self.data[:, :, idx_lon1]
            else:
                self.data = self.data[:,idx_lon1]
            self.psurf = self.psurf[:, idx_lon1]
        if self.latbnd[0] != self.latbnd[1]:
            tmp = list(np.abs(self.lat - self.latbnd[1]))
            idx_lat2 = np.argmin(tmp)
            self.lat = self.lat[idx_lat1:idx_lat2]
            if len(self.data.shape) == 3:
                self.data = self.data[:, idx_lat1:idx_lat2, :]
            elif len(self.data.shape) == 2:
                if self.lonbnd[0] == self.lonbnd[1]:
                    self.data = self.data[:, idx_lat1:idx_lat2]
                else:
                    self.data = self.data[idx_lat1:idx_lat2, :]
            elif len(self.data.shape) == 1:
                self.data = self.data[idx_lat1:idx_lat2]
            else:
                raise Exception("Problème avec la dimension de la variable dans le netcdf")
            if self.lonbnd[0] == self.lonbnd[1]:
                self.psurf = self.psurf[idx_lat1:idx_lat2]
            else:
                self.psurf = self.psurf[idx_lat1:idx_lat2, :]
        else:
            self.lat = self.lat[idx_lat1]
            if len(self.data.shape) == 3:
                self.data = self.data[:, idx_lat1, :]
            elif len(self.data.shape) == 2:
                if self.lonbnd[0] == self.lonbnd[1]:
                    self.data = self.data[:, idx_lat1]
                else:
                    self.data = self.data[idx_lat1, :]
            elif len(self.data.shape) == 1:
                self.data = self.data[idx_lat1]
            else:
                raise Exception("Problème avec la dimension de la variable dans le netcdf")
            if self.lonbnd[0] == self.lonbnd[1]:
                self.psurf = self.psurf[idx_lat1]
            else:
                self.psurf = self.psurf[idx_lat1, :]
        if dim == 3:    
            if self.levbnd[0] != self.levbnd[1]:
                tmp = list(np.abs(self.lev - self.levbnd[1]))
                idx_lev2 = np.argmin(tmp)
                self.lev = self.lev[idx_lev1:idx_lev2]
                self.a = self.a[idx_lev1:idx_lev2]
                self.b = self.b[idx_lev1:idx_lev2]
                if len(self.data.shape) == 3:
                    self.data = self.data[idx_lev1:idx_lev2, :, :]
                elif len(self.data.shape) == 2:
                    self.data = self.data[idx_lev1:idx_lev2, :]
                elif len(self.data.shape) == 1:
                    self.data = self.data[idx_lev1:idx_lev2]
                else:
                    raise Exception("Problème avec la dimension de la variable dans le netcdf")
            else:
                self.lev = self.lev[idx_lev1]
                self.a = self.a[idx_lev1]
                self.b = self.b[idx_lev1]
                if len(self.data.shape) == 3:
                    self.data = self.data[idx_lev1, :, :]
                elif len(self.data.shape) == 2:
                    self.data = self.data[idx_lev1, :]
                elif len(self.data.shape) == 1:
                    self.data = self.data[idx_lev1]
                else:
                    raise Exception("Problème avec la dimension de la variable dans le netcdf") 

    def convert_data(self, ds):
        unit = ds[self.var[0]].units
        if self.var[1] != '1':
            if self.var[1] == 'DU' and self.var[0][-3:] =='_tc':
                self.unit = self.var[1]
                if unit == 'molec m-2':
                    self.data = self.data / 2.6867e20
            else:
                raise Exception ("Convert {} n'est pas implémenté")
        else:
            self.unit = unit

    def cmp_vert_press(self):
        self.press = np.empty_like(self.lev)
        for i in range(len(self.lev)):
            self.press[i] = np.mean(self.psurf[:,:])*self.b[i] + self.a[i]
        self.vert = np.log(101325 / self.press) / 0.00012

    def mask_data(self):
        self.extend = 'both'
        if float(self.config_plot['vmin']) == 0. or (self.config_plot['maskmin'].lower() in ['true', 't'] and self.config_plot['maskmax'].lower() in ['false', 'f']):
            self.extend = 'max'
        elif self.config_plot['maskmin'].lower() in ['true', 't'] and self.config_plot['maskmax'].lower() in ['true', 't']:
            self.extend = None
        else:
            self.extend = 'min'
        if self.config_plot['maskmin'].lower() in ['true', 't']:
            vmin = float(self.config_plot['vmin'])
            self.data[self.data < vmin] = np.nan
        if self.config_plot['maskmax'].lower() in ['true', 't']:
            vmax = float(self.config_plot['vmax'])
            self.data[self.data > vmax] = np.nan
        
    def process_netcdf(self, config_class):
        self.unit = None
        if self.var is not None and self.date is not None and self.pseudo is not None:
            ds = self.getfile(config_class)
            if self.config_nc['getfile'].lower() in ['t', 'true']:
                ds = xr.open_dataset(os.path.join(self.dirtmp, self.outfile_name))
            self.levbnd = [ds.coords['lev'].values[0],
                           ds.coords['lev'].values[-1]]
            self.lonbnd = [ds.coords['lon'].values[0],
                           ds.coords['lon'].values[-1]]
            self.latbnd = [ds.coords['lat'].values[0],
                           ds.coords['lat'].values[-1]]
            self.cmp_boundaries(config_class)
            self.selectdata(ds)
            self.cmp_vert_press()
            self.convert_data(ds)
            self.mask_data()
        else:
            self.levbnd = [1, 60]
            self.lonbnd = [-180., 180.]
            self.latbnd = [-90., 90.]
            self.cmp_boundaries(config_class)

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

                             
        
        
                             
                                     
        
        
