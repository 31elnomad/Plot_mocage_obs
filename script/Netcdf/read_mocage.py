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
    self.nligne = int(config_class.config['global']['nligne'])
    self.ncol = int(config_class.config['global']['ncol'])
    if config_class.config['global']['type_plot'] == "map":
      self.config_plot = config_class.config['map']
    elif config_class.config['global']['type_plot'] == 'cut':
      self.config_plot = config_class.config['cut']
