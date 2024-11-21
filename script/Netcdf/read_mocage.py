#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""

import os
import sys
sys.path.append(os.path.abspath("../"))
from read_config import Config

class Netcdf_mocage(Config):

  def __init__(self, config_opts):
    Config.__init__(self, config_opts)
