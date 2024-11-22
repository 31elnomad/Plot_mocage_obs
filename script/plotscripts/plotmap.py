#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""
import multiprocessing
from multiprocessing import Process, Pool, Array
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from plotlist import list_of_plot

class PlotMap:
    
    def __init__(self, config_class):
        self.nligne = int(config_class.config['global']['nligne'])
        self.ncol = int(config_class.config['global']['ncol'])
        self.config_plot = config_class.config['map']
        self.listvar = self.config_plot['listvar'].split(',')
        self.listexp = self.config_plot['listexp'].split(',')
        self.order = self.config_plot['order'].split(',')
        self.listdate = config_class.listdate
        self.boundary = self.config_plot['boundary'].split('/')
        self.listlev = self.boundary[2].split(',')
        if self.listlev[0] == 'None':
            self.listlev = None
        elif self.listlev[0] != 'None' and self.listlev[1] == 'None':
            self.listlev = [int(self.listlev[0])]
        elif self.listlev[0] != 'None' and self.listlev[1] != 'None':
            if self.listlev[0] == self.listlev[1]:
                self.listlev = [int(self.listlev[0])]
            else:
                self.listlev = np.arange(int(self.listlev[0]), int(self.listlev[1]))
        
        self.param_plot_obj = list_of_plot(self.order,
                                          self.listvar,
                                          self.listexp,
                                          self.listdate,
                                          self.listlev,
                                          self.nligne,
                                          self.ncol,
                                          'map'
                                          )

    def create_fig(self):
        figsize = self.config_plot['figsize'].split(',')
        figsize = (int(figsize[0]), int(figsize[1]))
        self.proj = self.config_plot['projection'].split(':')
        if self.proj[0] in ['PlateCarree']:
            subplot_kw = {'projection': ccrs.PlateCarree(
                            central_longitude=float(self.proj[1]))
                        }
        elif self.proj[0] in ['Orthographic']:
            subplot_kw={'projection': ccrs.Orthographic(
                            central_longitude=float(self.proj[1].split('/')[0]),
                            central_latitude=float(self.proj[1].split('/')[1]))
                        }
        else:
            raise Exception("{} projection is unknown".format(self.proj[0]))
        self.fig, self.axs = plt.subplots(
                                    ncols = self.ncol,
                                    nrows = self.nligne,
                                    figsize = figsize,
                                    sharex = True,
                                    sharey = True,
                                    subplot_kw = subplot_kw)

    def create_list_param(self):
        print(self.param_one_plot[0])
        keys1 = list(self.param_one_plot[0].keys())[0]
        keys2 = list(self.param_one_plot[1].keys())[0]
        keys3 = list(self.param_one_plot[2].keys())[0]
        if len(self.param_one_plot) == 5:
            keys4 = list(self.param_one_plot[3].keys())[0]
        list_param_plot = np.empty_like(self.param_one_plot)
        list_param_plot[:] = None
        list_param_plot = list_param_plot.tolist()
        self.param = np.empty(self.nligne*self.ncol)
        self.param = self.param.tolist()
        for j in range(self.nligne):
            for i in range(self.ncol):
                print(self.param_one_plot[0][keys1])
                quit()
                list_param_plot[0] = self.param_one_plot[0][keys1][i]
                list_param_plot[1] = self.param_one_plot[1][keys2][j]
                list_param_plot[2] = self.param_one_plot[2][keys3][0]
                list_param_plot[-1] = self.param_one_plot[-1]
                if len(self.param_one_plot) == 5:
                    list_param_plot[3] = self.param_one_plot[3][keys4][0]
                self.param[self.ncol*j + i] = list_param_plot
        print(self.param)

    def __main_plotmap__(self, param_one_plot):
        self.param_one_plot = param_one_plot
        self.create_fig()
        self.create_list_param()
        

            
       


    

        
        

            
       
            
            
        
            
    
        
        
