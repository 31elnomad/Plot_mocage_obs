#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""
class Plot:

  def __init__(self, config_class):
    exp = False
    for plot in config_class.config["global"]["plot_list"].split(","):
        if "exp" in config_class.config[plot]['listexp']:
          from read_mocage import Netcdf_mocage
          exp = True
    if exp is True:
      nc_class = Netcdf_mocage(config_class)
    
