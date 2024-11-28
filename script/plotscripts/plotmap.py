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
        self.config_class = config_class
        self.nligne = int(config_class.config['global']['nligne'])
        self.ncol = int(config_class.config['global']['ncol'])
        self.config_plot = config_class.config['map']
        self.listvar = self.config_plot['listvar'].split(',')
        self.listexp = self.config_plot['listexp'].split(',')
        self.order = self.config_plot['order'].split(',')
        self.grid = self.config_plot['grid'].split(',')
        self.listdate = config_class.listdate
        self.boundary = self.config_plot['boundary'].split('/')
        self.proj = self.config_plot['projection'].split(':')
        if self.boundary[2] == 'None':
            self.listlev = None
        else:
            self.listlev = self.boundary[2].split(',')
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
            self.mapproj = ccrs.PlateCarree(
                            central_longitude=float(self.proj[1]))
            self.subplot_kw = {'projection': self.mapproj}
        elif self.proj[0] in ['Orthographic']:
            self.mapproj = ccrs.Orthographic(
                            central_longitude=float(self.proj[1].split('/')[0]),
                            central_latitude=float(self.proj[1].split('/')[1]))
            self.subplot_kw={'projection': self.mapproj}
        else:
            raise Exception("{} projection is unknown".format(self.proj[0]))
        self.fig, self.axs = plt.subplots(
                                    ncols = self.ncol,
                                    nrows = self.nligne,
                                    figsize = figsize,
                                    sharex = True,
                                    sharey = True,
                                    subplot_kw = self.subplot_kw)

    def create_list_param(self):
        # Extraction des clés de chaque dictionnaire
        keys1 = list(self.param_one_plot[0].keys())[0]
        keys2 = list(self.param_one_plot[1].keys())[0]
        keys3 = list(self.param_one_plot[2].keys())[0]
        # Gestion conditionnelle de la 4e clé si nécessaire
        keys4 = None
        if len(self.param_one_plot) == 5:
            keys4 = list(self.param_one_plot[3].keys())[0]
        # Initialisation de self.param
        self.param = []
        # Boucles pour construire list_param_plot
        for j in range(self.nligne):
            for i in range(self.ncol):
                # Créer une nouvelle liste à chaque itération
                list_param_plot = [None] * (len(self.param_one_plot)+2)
                # Remplissage des paramètres en fonction des indices
                list_param_plot[0] = self.param_one_plot[0][keys1][i]  # Variable selon 'i'
                list_param_plot[1] = self.param_one_plot[1][keys2][j]  # Variable selon 'j'
                list_param_plot[2] = self.param_one_plot[2][keys3][0]  # Premier élément (fixe)
                # Ajout du dernier paramètre commun
                list_param_plot[-1] = self.param_one_plot[-1]
                list_param_plot[-2] = j # ligne
                list_param_plot[-3] = i # col
                # Gestion conditionnelle du 4e paramètre
                if len(self.param_one_plot) == 5:
                    list_param_plot[3] = self.param_one_plot[3][keys4][0]  # Premier élément (fixe)
                # Ajouter la liste au résultat final
                self.param.append(list_param_plot)
                # Affichage pour vérification
                print(f"Paramètre ajouté : {list_param_plot}")

    def cut_list(self, List):
        if len(List) == 6:
            if List[-1] in ['map_1', 'map_6']:
                self.pseudo = List[0]
            elif List[-1] in ['map_2', 'map_5']:
                self.pseudo = List[1]
            elif List[-1] in ['map_3', 'map_4']:
                self.pseudo = List[2]
            if List[-1] in ['map_2', 'map_4']:
                self.date = List[0] 
            elif List[-1] in ['map_1', 'map_3']:
                self.date = List[1] 
            elif List[-1] in ['map_5', 'map_6']:
                self.date = List[2]
            if List[-1] in ['map_3', 'map_5']:
                self.var = List[0] 
            elif List[-1] in ['map_4', 'map_6']:
                self.var = List[1] 
            elif List[-1] in ['map_1', 'map_2']:
                self.var = List[2] 
        else:
            raise Exception("List avec 7 éléments pas encore codé dnas plotmap.py")
        if self.pseudo != "None":
            self.pseudo = self.pseudo.split(':')
        else:
            self.pseudo = None
        if self.date == "None":
            self.date = None
        if self.var != "None":
            self.var = self.var.split(':')
        else:
            self.var = None

    def plot_para(self, List):
        self.cut_list(List)
        idx = List[-3] + List[-2]*self.ncol
        from set_cartopy import _set_cartopy_
        fig, ax = plt.subplots(ncols = 1,
                               nrows = 1,
                               subplot_kw = self.subplot_kw)

        if self.pseudo is not None and self.var is not None and self.date is not None:
            if self.pseudo[0] in ['exp']:
                from read_mocage import Netcdf_mocage
                obj_data = Netcdf_mocage(self.config_class,
                                              self.pseudo,
                                              self.date,
                                              self.var)
                obj_data.process_netcdf(self.config_class)  
                ax = _set_cartopy_(self, obj_data, ax, List[-3], List[-2], idx)
                if self.config_plot['plot_opt'].split(':')[0] in ['contourf']:
                    from plot2d import __contourf__, __print_colorbar__
                    pas = float(self.config_plot['plot_opt'].split(':')[1])
                    vmin = float(self.config_plot['vmin'])
                    vmax = float(self.config_plot['vmax'])
                    ax, sc = __contourf__(ax, obj_data, pas, vmin, vmax, transform=self.mapproj, cmap=self.config_plot['cmap'])
                    if 'var' in self.order[:2] or 'lev' in self.order[:2]:
                        cbar = __print_colorbar__(fig, sc, self.config_plot, obj_data)
                        if unit is not None:
                            cbar.set_label("{} ({})".format(self.var[0], obj_data.unit))
                        else:
                            cbar.set_label("{}".format(self.var[0]))
        else:
            from read_mocage import Netcdf_mocage
            obj_data = Netcdf_mocage(self.config_class,
                                      self.pseudo,
                                      self.date,
                                      self.var)
            obj_data.process_netcdf(self.config_class)  
            ax = _set_cartopy_(self, obj_data, ax, List[-3], List[-2], idx)
            sc = None
        filename = f"subplot_{idx}.png"
        plt.savefig(filename)
        plt.close()
        return filename, sc, obj_data, self.var, obj_data.unit
        



    def __main_plotmap__(self, param_one_plot):
        self.param_one_plot = param_one_plot
        self.create_fig()
        self.create_list_param()
        with Pool(5) as p:
            results = p.map(self.plot_para, self.param)
        from concat_plot import __concat_plot__
        from plot2d import __print_colorbar__
        from plot_opts import process_res
        filenames, sc, obj_data, var, unit = process_res(results)
        self.axs = __concat_plot__(self.fig, self.axs, filenames)
        plt.tight_layout()
        if 'var' not in self.order[:2] and 'lev' not in self.order[:2]:
            cbar = __print_colorbar__(self.fig, sc, self.config_plot, obj_data)
            if unit is not None:
                cbar.set_label("{} ({})".format(var, unit))
            else:
                cbar.set_label("{}".format(var))
        plt.savefig('test.png')
        plt.close()
        
        

            
       


    

        
        

            
       
            
            
        
            
    
        
        
