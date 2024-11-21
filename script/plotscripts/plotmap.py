#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""

from functions import list_of_plot

class PlotMap:
    
    def __init__(self, config_class):
        self.nligne = int(config_class.config['global']['nligne'])
        self.ncol = int(config_class.config['global']['ncol'])
        self.config_plot = config_class.config['map']
        self.listvar = self.config_plot['listvar'].split(',')
        self.listexp = self.config_plot['listexp'].split(',')
        self.order = self.config_plot['order'].split(',')

        list_of_plot(self.order,
                     self.listvar,
                     self.listexp,
                     self.listdate,
                     self.nligne,
                     self.ncol
        

            
       
            
            
        
            
    
        
        
