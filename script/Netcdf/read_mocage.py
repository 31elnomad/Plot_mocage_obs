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
    for plot in config_class.config["global"]["plot_list"].split(","):
      print(config_class.config[plot]["listexp"])
      
