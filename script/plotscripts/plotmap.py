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
                list_param_plot = [None] * len(self.param_one_plot)
                # Remplissage des paramètres en fonction des indices
                list_param_plot[0] = self.param_one_plot[0][keys1][i]  # Variable selon 'i'
                list_param_plot[1] = self.param_one_plot[1][keys2][j]  # Variable selon 'j'
                list_param_plot[2] = self.param_one_plot[2][keys3][0]  # Premier élément (fixe)
                # Ajout du dernier paramètre commun
                list_param_plot[-1] = self.param_one_plot[-1]
                # Gestion conditionnelle du 4e paramètre
                if len(self.param_one_plot) == 5:
                    list_param_plot[3] = self.param_one_plot[3][keys4][0]  # Premier élément (fixe)
                # Ajouter la liste au résultat final
                self.param.append(list_param_plot)
                # Affichage pour vérification
                print(f"Paramètre ajouté : {list_param_plot}")

    def plot_para(self, List):
        self.cut_list()
        print(self.exp, self.date, self.var)

    def cut_list(self, List):
        if len(List) == 4:
            if List[-1] in ['map_1', 'map_6']:
                self.exp = List[0]
            elif List[-1] in ['map_2', 'map_5']:
                self.exp = List[1]
            elif List[-1] in ['map_3', 'map_4']:
                self.exp = List[2]
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
            raise Exception("List avec 5 éléments pas encore codé dnas plotmap.py")


        

    def __main_plotmap__(self, param_one_plot):
        self.param_one_plot = param_one_plot
        self.create_fig()
        self.create_list_param()
        with Pool(5) as p:
            results = p.map(self.plot_para, self.param)
        

            
       


    

        
        

            
       
            
            
        
            
    
        
        
