#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21

@author: baclesm
"""
import collections
import numpy as np

def list_of_plot(order, listvar, listexp, listdate, nligne, ncol):

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

    def number_plot(order, listvar, listexp, listdate, nligne, ncol):
        print("map, order: {}".format(order))
        if len(order) == 3:
            test = collections.Counter(['var', 'exp', 'date']) == collections.Counter(order)
            if test is False:
                raise Exception("Problème avec la variable order dans la section map. Doit contenir 'var', 'exp' et 'date'.")
             output_dict = __order_length_3__(order, listvar, listexp, listdate, nligne, ncol)
        elif len(order) == 4:
            test = collections.Counter(['var', 'exp', 'date', 'lev']) == collections.Counter(order)
            if test is False:
                raise Exception("Problème avec la variable order dans la section map. Doit contenir 'var', 'exp', 'lev' et 'date'.")
            ####fonction listplot_2d
        return output_dict

    def __order_length_3__(order, listvar, listexp, listdate, nligne, ncol):  

        def number_plot_3(order, listvar, listexp, listdate, nligne, ncol):
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
    
        def param_per_plot_3(list_dim, order, listvar, listexp, listdate, nligne, ncol, case):
            ouput_dict = {}
            for x in range(list_dim[1]):
                for y in range(list_dim[2]):
                    for z in range(list_dim[0]):
                        ouput_dict[str((x+1)*(y+1)*(z+1))] = listdict_param(case,
                                                                            listvar,
                                                                            listexp,
                                                                            listdate,
                                                                            nligne,
                                                                            ncol,
                                                                            x,
                                                                            y,
                                                                            z)
            return ouput_dict
    
        def listdict_param_3(case, listvar, listexp, listdate, nligne, ncol, x, y, z):
            nsubplot = [ncol, nligne]
            if case in [1, 2]:
                var1 = 'var'
                list1 = [listvar[z]]
            elif case in [3, 4]:
                var1 = 'exp'
                list1 = [listexp[z]]
            elif case in [5, 6]:
                var1 = 'date'
                list1 = [listdate[z]]
            if case in [1, 6]:
                var2 = 'exp'
                list2 = __listdict_param__(listexp, x, ncol)
            elif case in [2, 4]:
                var2 = 'date'
                list2 = __listdict_param__(listdate, x, ncol)
            elif case in [3, 5]:
                var2 = 'var'
                list2 = __listdict_param__(listvar, x, ncol)
            if case in [1, 3]:
                var3 = 'date'
                list3 = __listdict_param__(listdate, y, nligne)
            elif case in [2, 5]:
                var3 = 'exp'
                list3 = __listdict_param__(listexp, y, nligne)
            elif case in [4, 6]:
                var3 = 'var'
                list3 = __listdict_param__(listvar, y, nligne)
            output = [{var1: list1},
                      {var2: list2},
                      {var3: list3},
                      case]
            return output
            
        list_dim, case = number_plot_3(order, listvar, listexp, listdate, nligne, ncol)  
        ouput_dict = param_per_plot_3(list_dim, order, listvar, listexp, listdate, nligne, ncol, case)
        return output_dict
        
    output_dict = number_plot(order, listvar, listexp, listdate, nligne, ncol)
    return ouput_dict


  
