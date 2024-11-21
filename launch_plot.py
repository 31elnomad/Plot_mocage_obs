#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on the Wed Nov 20

@author baclesm
"""
import argparse
import os
import sys
sys.path.append(os.path.abspath("script"))
from read_config import Config

def create_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-cfg', '--cfg',
                        help='config_file',
                        metavar='cfg')
    parser.add_argument('-start', '--start',
                         nargs='?', const=None,
                         help='date du début',
                         metavar='start')
    parser.add_argument('-end', '--end',
                        nargs='?', const=None,
                        help='date de fin',
                        metavar='end')      
    parser.add_argument('-deltat', '--deltat',
                        nargs='?', const=None,
                        help='pas de temps',
                        metavar='deltat')
    parser.add_argument('-listdate', '--listdate',
                        nargs='?', const=None,
                        help='list de date',
                        metavar='listdate')
    config_opts = parser.parse_args()
    return config_opts

def add_path(config_class):
    # exec_path = os.getcwd()
    for plot in config_class.config["global"]["plot_list"].split(","):
        if "exp" in config_class.config[plot]['listexp']:
            if os.path.abspath("script/Netcdf") not in sys.path:
                print("Ajout du répertoire 'Netcdf' au pythonpath")
                sys.path.append(os.path.abspath("script/Netcdf"))            
    
if __name__ == "__main__":
    config_opts = create_argparse()
    config_class = Config(config_opts)
    add_path(config_class)
    
    
