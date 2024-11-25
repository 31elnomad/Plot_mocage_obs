#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""

import os
import sys
import datetime

class Netcdf_mocage:

    def __init__(self, config_class, pseudo, date, var):
        self.config_nc = config_class.config[pseudo]
        self.pseudo = pseudo
        self.date = datetime.datetime(int(date[:4]),
                                      int(date[4:6]),
                                      int(date[6:8]),
                                      int(date[8:10])) # 2024010100
        self.var = var #SO_2_tc:DU,SO_2:1e9
        self.domain = self.config_nc['domain']
        self.user = self.config_nc['user']
        self.tree = self.config_nc['tree']
        if self.tree not in ['script']:
            self.conf = self.config_nc['conf']
            self.nameexp = self.config_nc['nameexp']
            self.suffix = self.config_nc['suffix']
            self.group = self.config_nc['group']
            self.reseau = self.config_nc['reseau']
            self.echeance = int(self.config_nc['echeance'])
        elif self.tree in ['script']:
            self.type_exp = self.config_nc['typeexp'].lower()
            self.type_file = self.config_nc['type_file']
            self.wlength = None
            if self.type_exp.lower() not in ['direct']:
                self.wlength = int(self.config_nc['wlength'])

    def create_directory(self):
        if self.tree in ['scripts']:
            self.indir = f'/home/{self.user}/MOCAGEHM/{self.nameexp}/'
        elif self.tree in ['vortex']:
            self.indir = f'/home/{self.user}/vortex/mocage/{self.conf}/{self.nameexp}.upper()/'
            d = self.date - datetime.timedelta(hours=self.echeance)
            self.indir += d.strftime("%Y%m%d") + 'T'
            self.indir += self.reseau.zfill(4) + self.suffix + '/' + self.group
        elif self.tree.upper() in ['OPER', 'MIRR', 'DBLE']:
            self.indir = f'/chaine/mxpt/mxpt001/vortex/mocage/{self.conf}/{self.tree.upper()}/'
            self.indir += f'{self.datet.year}/{str(self.date.month).zfill(2)}/'
            self.indir += f'{str(self.date.day).zfill(2)}/T'
            self.indir += self.reseau.zfill(4) + self.suffix + '/' + self.group
        else:
            raise Exception("{} est inconnu ou non implémenté".format(self.tree))

    def create_filename(self):
        self.create_directory()
        if self.type_file in ['PPS1']:
            self.filename1 = f'ppstats.mocage-first_level.{self.domain}+0024.netcdf'
        elif self.type_file in ['HMnc']:
            if self.tree in ['script']:
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
            else:
                echeance = int(self.date.hour) + self.echeance
                self.filename1 = f'grid.mocage-forecast.{self.domain.lower()} + {str(echeance).zfill(4)}:00.netcdf'

    def getfile(self, config_class):
        print(self.namexp, self.Date, self.indir, self.filename1)
        self.dirtmp = config_class.config['global']['tmp_repository'].split('/')
        print(self.dirtmp)
        quit()
                                   
        
                        

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

                             
        
        
                             
                                     
        
        
