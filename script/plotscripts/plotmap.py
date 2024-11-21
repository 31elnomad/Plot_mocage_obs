#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""
import collections

class PlotMap:
    
    def __init__(self, config_class):
        self.nligne = int(config_class.config['global']['nligne'])
        self.ncol = int(config_class.config['global']['ncol'])
        self.config_plot = config_class.config['map']
        self.listvar = self.config_plot['listvar'].split(',')
        self.listexp = self.config_plot['listexp'].split(',')
        self.order = self.config_plot['order'].split(',')

        self.number_plot()
        
        """# Initialisation d'un indicateur pour savoir si une expérience est trouvée
        is_experiment_found = any(
            "exp" in config_class.config[plot]['listexp']
            for plot in self.plot_list
        )
        if is_experiment_found:
            # Import conditionnel
            from read_mocage import Netcdf_mocage
            self.nc_class = Netcdf_mocage(config_class)
        else:
            self.nc_class = None"""

    def number_plot(self):
        print("map, order: {}".format(self.order))
        test = collections.Counter(['var', 'exp', 'date']) == collections.Counter(self.order)
        if len(self.order) != 3 or test is False:
            raise Exception("Problème avec la variable order dans la section map. Doit contenir 'var', 'exp' et 'date'.")
        for element in self.order:
            idx = self.order.index(element)
            print(element, idx)
       
            
            
        
            
    
        
        
