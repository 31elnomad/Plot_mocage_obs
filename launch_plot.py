#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on the Wed Nov 20

@author baclesm
"""
import argparse
import os
import sys
sys.path.append(os.path.abspath("script/Netcdf"))
from read_mocage import Netcdf_mocage

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
    
if __name__ == "__main__":
    config_opts = create_argparse()
    config_class = Netcdf_mocage(config_opts)
    print(config_class.__dict__)
    print(config_class.config['global'])
    
    
