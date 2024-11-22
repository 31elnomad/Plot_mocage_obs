#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""
import multiprocessing
from multiprocessing import Process, Pool, Array
import numpy as np
from plotlist import list_of_plot

class PlotMap:
    
    def __init__(self, config_class):
        self.nligne = int(config_class.config['global']['nligne'])
        self.ncol = int(config_class.config['global']['ncol'])
        self.config_plot = config_class.config['map']
        self.listvar = self.config_plot['listvar'].split(',')
        self.listexp = self.config_plot['listexp'].split(',')
        self.order = self.config_plot['order'].split(',')
        self.listdate = config_class.listdate
        self.boundary = cofig_class.config['map']['boundary'].split('/')
        self.listlev = self.boundary[2].split(',')
        if self.listlev[0] == 'None':
            self.listlev = None
        elif self.listlev[0] != 'None' and self.listlev[1] == 'None':
            self.listlev = [int(self.listlev[0]]
        elif self.listlev[0] != 'None' and self.listlev[1] != 'None':
            if self.listlev[0] == self.listlev[1]:
                self.listlev = [int(self.listlev[0]]
            else:
                self.listlev = np.arange(int(self.listlev[0]), int(self.listlev[1]))
        
        self.list_dim, self.output = list_of_plot(self.order,
                                                  self.listvar,
                                                  self.listexp,
                                                  self.listdate,
                                                  self.listlev,
                                                  self.nligne,
                                                  self.ncol
                                                 )


    

        
        

            
       
            
            
        
            
    
        
        
