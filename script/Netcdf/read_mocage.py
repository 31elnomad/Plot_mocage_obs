#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""

import os
import sys

class Netcdf_mocage:
  def __init__(self, config_class):
    self.plot = {}
    for plot in config_class.config["global"]["plot_list"].split(","):
      if plot == "map":
        self.config_map = config_class.config[plot]
        self.case == int(config_class.config
      print(config_class.config[plot]["listexp"])
      
