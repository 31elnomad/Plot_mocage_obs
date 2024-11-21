#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""
import collections
import numpy as np

def list_of_plot(order, listvar, listexp, listdate, nligne, ncol):

    def number_plot(order, listvar, listexp, listdate, nligne, ncol):
        print("map, order: {}".format(order))
        test = collections.Counter(['var', 'exp', 'date']) == collections.Counter(order)
        if len(order) != 3 or test is False:
            raise Exception("Problème avec la variable order dans la section map. Doit contenir 'var', 'exp' et 'date'.")
        if order[0] == 'var':
            plotz = len(listvar)
            if order[1] == 'exp':
              plotx = cmp_nplot(listexp, ncol)
              ploty = cmp_nplot(listdate, nligne)
            elif order[1] == 'date':
              plotx = cmp_nplot(listdate, ncol)
              ploty = cmp_nplot(listexp, nligne)   
        elif order[0] == 'exp':
            plotz = len(listexp)
            if order[1] == 'var':
                plotx = cmp_nplot(listvar, ncol)
                ploty = cmp_nplot(listdate, nligne)
            elif order[1] == 'date':
                plotx = cmp_nplot(listdate, ncol)
                ploty = cmp_nplot(listvar, nligne)  
        elif order[0] == 'date':
            plotz = len(listdate)
            if order[1] == 'var':
                plotx = cmp_nplot(listvar, ncol)
                ploty = cmp_nplot(listexp, nligne)
            elif order[1] == 'exp':
                plotx = cmp_nplot(listexp, ncol)
                ploty = cmp_nplot(listvar, nligne)  
        return [plotz, plotx, ploty]
    
    def cmp_nplot(list, number):
        """
        list = listvar, listdate or lisexp
        number = self.ncol ou self.nligne
        """
        n = len(list) // number
        if len(list) % number > 0:
          n = n + 1
        return n

    def param_per_plot(list_dim, order, listvar, listexp, listdate, nligne, ncol):
        param_plot_dict = {}
        for z, x, y in zip(list(np.arange(list_dim[0])), list(np.arange(list_dim[1])), list(np.arange(list_dim[2]))):
            print(z, x, y)
        
    list_dim = number_plot(order, listvar, listexp, listdate, nligne, ncol)  
    param_per_plot(list_dim, order, listvar, listexp, listdate, nligne, ncol)
    
    return list_dim


  
