#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""
class Plot:
    
    def __init__(self, config_class):
        self.nligne = int(config_class.config['global']['nligne'])
        self.ncol = int(config_class.config['global']['ncol'])
        self.config_plot = config_class.config['map']
        self.listvar = self.config_plot['listvar'].split(',')
        self.listexp = self.config_plot['listexp'].split(',')
        self.case = int(self.config_plot['case'])
        
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
            self.nc_class = None"""self.plot_list = config_class.config["global"]["plot_list"].split(",")

    def number_plot(self):
        print("map, case {}".format(self.case))
        if self.case == 1:
            nplot_x = len(self.listexp) // self.ncol + 1
            nplot_y = len(self.listdate) // self.nligne + 1
            nplot = len(self.listvar) * nplot_x * nplot_y
        elif self.case == 2:
            nplot_x = len(self.listexp) // self.ncol + 1
            nplot_y = len(self.listvar) // self.nligne + 1
            nplot = len(self.listdate) * nplot_x * nplot_y
        elif self.case == 3:
            nplot_x = len(self.listvar) // self.ncol + 1
            nplot_y = len(self.listdate) // self.nligne + 1
            nplot = len(self.listexp) * nplot_x * nplot_y
        else:
            raise Exception("Case doit valoir 1, 2 ou 3 pour les cartes")

    def param_to_plot(self):
        
            
    
        
        
