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
                case = 1
            elif order[1] == 'date':
                plotx = cmp_nplot(listdate, ncol)
                ploty = cmp_nplot(listexp, nligne)  
                case = 2
        elif order[0] == 'exp':
            plotz = len(listexp)
            if order[1] == 'var':
                plotx = cmp_nplot(listvar, ncol)
                ploty = cmp_nplot(listdate, nligne)
                case = 3
            elif order[1] == 'date':
                plotx = cmp_nplot(listdate, ncol)
                ploty = cmp_nplot(listvar, nligne) 
                case = 4
        elif order[0] == 'date':
            plotz = len(listdate)
            if order[1] == 'var':
                plotx = cmp_nplot(listvar, ncol)
                ploty = cmp_nplot(listexp, nligne)
                case = 5
            elif order[1] == 'exp':
                plotx = cmp_nplot(listexp, ncol)
                ploty = cmp_nplot(listvar, nligne)  
                case = 6
        return [plotz, plotx, ploty], case
    
    def cmp_nplot(list, number):
        """
        list = listvar, listdate or lisexp
        number = self.ncol ou self.nligne
        """
        n = len(list) // number
        if len(list) % number > 0:
          n = n + 1
        return n

    def param_per_plot(list_dim, order, listvar, listexp, listdate, nligne, ncol, case):
        param_plot_dict = {}
        for x in range(list_dim[1]):
            for y in range(list_dim[2]):
                for z in range(list_dim[0]):
                    param_plot_dict[str((x+1)*(y+1)*(z+1))] = listdict_param(case,
                                                                             listvar,
                                                                             listexp,
                                                                             listdate,
                                                                             nligne,
                                                                             ncol,
                                                                             x,
                                                                             y,
                                                                             z)

    def listdict_param(case, listvar, listexp, listdate, nligne, ncol, x, y, z):
        if case == 1:
            var1 = 'var'
            list1 = listvar[z]
            var2 = 'exp'
            var3 = 'date'
            if len(listexp[ncol*x:]) <= ncol:
                list2 = listexp[ncol*x:]
            else:
                list2 = listexp[ncol*x:ncol*(x+1)]
            if len(listdate[nligne*y:]) <= nligne:
                list3 = listexp[nligne*y:]
            else:
                list3 = listexp[nligne*y:nligne*(y+1)]
        output = [{var1: list1},
                  {var2: list2},
                  {var3: list3}]
        print(output)
        return output
        
    list_dim, case = number_plot(order, listvar, listexp, listdate, nligne, ncol)  
    param_per_plot(list_dim, order, listvar, listexp, listdate, nligne, ncol, case)
    
    return list_dim


  
