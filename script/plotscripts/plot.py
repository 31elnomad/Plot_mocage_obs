#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""
class Plot:
    def __init__(self, config_class):
        self.plot_list = config_class.config["global"]["plot_list"].split(",")
        # Initialisation d'un indicateur pour savoir si une expérience est trouvée
        is_experiment_found = any(
            "exp" in config_class.config[plot]['listexp']
            for plot in self.plot_list
        )
        if is_experiment_found:
            # Import conditionnel
            from read_mocage import Netcdf_mocage
            self.nc_class = Netcdf_mocage(config_class)
        else:
            self.nc_class = None
