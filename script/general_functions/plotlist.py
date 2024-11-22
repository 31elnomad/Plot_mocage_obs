#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""
import collections
import numpy as np

class list_of_plot:

    def __init__(self, order, listvar, listexp, listdate, listlev, nligne, ncol, plot_type):
        self.order = order
        self.listvar = listvar
        self.listexp = listexp
        self.listdate = listdate
        self.listlev = listlev
        self.nligne = nligne
        self.ncol = ncol
        self.plot_type = plot_type
        self.output_dict = self.compute_param_plot()

    def compute_param_plot(self):
        print("order: {}".format(self.order))
        if self.plot_type in ['map']:
            if len(self.order) == 3:
                test = collections.Counter(['var', 'exp', 'date']) == collections.Counter(self.order)
                if test is False:
                    raise Exception("Problème avec la variable order dans la section map. Doit contenir 'var', 'exp' et 'date'.")
                output_dcict = self.__order_len_3_map__()
            elif len(order) == 4:
                test = collections.Counter(['var', 'exp', 'date', 'lev']) == collections.Counter(self.order)
                if test is False:
                    raise Exception("Problème avec la variable order dans la section map. Doit contenir 'var', 'exp', 'lev' et 'date'.")
                raise Exception ("{} n'est pas implémenté dans la fonction list_of_plot (script/general_functions/plotlist.py)".format(self.order))
            else:
                raise Exception ("Pour les maps, order doit obligatoirement contenir var, exp, date et lev pour le cas de variables 3D.")
        else:
            raise Exception ("{} n'est pas implémenté dans la fonction list_of_plot (script/general_functions/plotlist.py)".format(self.plot_type))
        return output_dict

    def __order_len_3_map__(self):
        def number_plot(self):
            if self.order[2] in ['var']:
                plotz = len(self.listvar)
                if self.order[0] == 'exp':
                    plotx = cmp_nplot(self.listexp, self.ncol)
                    ploty = cmp_nplot(self.listdate, self.nligne)
                    self.case = 1
                elif self.order[0] == 'date':
                    plotx = cmp_nplot(self.listdate, self.ncol)
                    ploty = cmp_nplot(self.listexp, self.nligne)  
                    self.case = 2
            elif order[2] == 'exp':
                plotz = len(self.listexp)
                if self.order[0] == 'var':
                    plotx = cmp_nplot(self.listvar, self.ncol)
                    ploty = cmp_nplot(self.listdate, self.nligne)
                    self.case = 3
                elif self.order[0] == 'date':
                    plotx = cmp_nplot(self.listdate, self.ncol)
                    ploty = cmp_nplot(self.listvar, self.nligne) 
                    self.case = 4
            elif self.order[2] == 'date':
                plotz = len(self.listdate)
                if self.order[0] == 'var':
                    plotx = cmp_nplot(self.listvar, self.ncol)
                    ploty = cmp_nplot(self.listexp, self.nligne)
                    self.case = 5
                elif self.order[0] == 'exp':
                    plotx = cmp_nplot(self.listexp, self.ncol)
                    ploty = cmp_nplot(self.listvar, self.nligne)  
                    self.case = 6
            self.list_dim = [plotx, ploty, plotz]
    
        def param_per_plot(self):
            ouput_dict = {}
            for x in range(self.list_dim[0]):
                for y in range(self.list_dim[1]):
                    for z in range(self.list_dim[2]):
                        ouput_dict[str((x+1)*(y+1)*(z+1))] = self.listdict_param(x,
                                                                                 y,
                                                                                 z)
            return output_dict
    
        def listdict_param(self, x, y, z):
            if self.case in [1, 2]:
                var3 = 'var'
                list3 = [self.listvar[z]]
            elif self.case in [3, 4]:
                var3 = 'exp'
                list3 = [self.listexp[z]]
            elif self.case in [5, 6]:
                var3 = 'date'
                list3 = [self.listdate[z]]
            if self.case in [1, 6]:
                var1 = 'exp'
                list1 = __listdict_param__(self.listexp, x, self.ncol)
            elif self.case in [2, 4]:
                var1 = 'date'
                list1 = __listdict_param__(self.listdate, x, self.ncol)
            elif self.case in [3, 5]:
                var1 = 'var'
                list1 = __listdict_param__(self.listvar, x, self.ncol)
            if self.case in [1, 3]:
                var2 = 'date'
                list2 = __listdict_param__(self.listdate, y, self.nligne)
            elif self.case in [2, 5]:
                var2 = 'exp'
                list2 = __listdict_param__(self.listexp, y, self.nligne)
            elif self.case in [4, 6]:
                var2 = 'var'
                list2 = __listdict_param__(self.listvar, y, self.nligne)
            output = [{var1: list1},
                      {var2: list2},
                      {var3: list3},
                      case]
            return output
        output_dict = param_per_plot()
        return output_dict

def cmp_nplot(list, number):
    """
    list = listvar, listdate or lisexp
    number = self.ncol ou self.nligne
    """
    n = len(list) // number
    if len(list) % number > 0:
      n = n + 1
    return n

def __listdict_param__(list, i, j):
    """
    i: valeur de x ou y
    j: valeur de ncol ou nligne
    """
    if len(list) - i * j == 1:
        l = [list[j*i]]
    elif len(list) - i * j <= j:
        l = list[j*i:]
    else:
        l = list[j*i:j*(i+1)]
    return l


  
