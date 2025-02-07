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
sys.path.append(os.path.abspath("script/plotscripts"))
sys.path.append(os.path.abspath("script/general_functions"))
from read_config import Config
from plotmap import  PlotMap
import os
import sys
import argparse
from configparser import ConfigParser

# Importez Config, Plot et Netcdf_mocage uniquement si ces fichiers existent
# Ajustez les imports si nécessaire pour votre structure de projet.

def create_argparse():
    """
    Crée un parseur pour les arguments en ligne de commande.
    """
    parser = argparse.ArgumentParser(description="Script pour générer des plots à partir d'une configuration.")
    
    parser.add_argument('-cfg', '--cfg',
                        required=True,  # Le fichier de configuration est obligatoire
                        help='Chemin vers le fichier de configuration',
                        metavar='cfg')
    parser.add_argument('-start', '--start',
                        help="Date de début au format 'YYYYMMDDHH'",
                        metavar='start')
    parser.add_argument('-end', '--end',
                        help="Date de fin au format 'YYYYMMDDHH'",
                        metavar='end')      
    parser.add_argument('-deltat', '--deltat',
                        type=int,
                        help="Pas de temps en heures (entier)",
                        metavar='deltat')
    parser.add_argument('-listdate', '--listdate',
                        help="Liste de dates séparées par des virgules",
                        metavar='listdate')
    
    return parser.parse_args()

def add_path(config_class):
    """
    Ajoute les chemins nécessaires au PYTHONPATH et importe les modules conditionnels.
    """
    ext_package = config_class.config['global']['ext_package'].split(',')
    for pack in ext_package:
        path = pack.split(':')
        if path[1] not in sys.path:
            print("Ajout de {} à sys.apth".format(path[1]))
            sys.path.append(path[1])
    # Vérifie si 'Netcdf' doit être ajouté au PYTHONPATH
    plot = config_class.config["global"]["type_plot"]
    if plot in ["map", "cut"]:
        if "exp" in config_class.config[plot].get('listexp', ''):
            netcdf_path = os.path.abspath("script/Netcdf")
            if netcdf_path not in sys.path:
                print("Ajout du répertoire 'Netcdf' au PYTHONPATH")
                sys.path.append(netcdf_path)
        if "obs" in config_class.config[plot].get('listexp', ''):
            obs_path = os.path.abspath("script/observations")
            if obs_path not in sys.path:
                print("Ajout du répertoire 'observations' au PYTHONPATH")
                sys.path.append(obs_path)

if __name__ == "__main__":
    # Crée et parse les arguments
    config_opts = create_argparse()
    
    # Initialise la classe Config
    try:
        config_class = Config(config_opts)
    except Exception as e:
        print(f"Erreur lors de l'initialisation de Config : {e}")
        sys.exit(1)
    
    # Ajoute les chemins et initialise les modules conditionnels
    try:
        add_path(config_class)
    except Exception as e:
        print(f"Erreur lors de l'ajout des chemins ou des imports conditionnels : {e}")
        sys.exit(1)
    if config_class.config["global"]["type_plot"] == 'map':
        # Initialise la classe PlotMap
        plot_class = PlotMap(config_class)
        try:
            plot_class = PlotMap(config_class)
        except Exception as e:
            print(f"Erreur lors de l'initialisation de PlotMap : {e}")
            sys.exit(1)
        param_plot = plot_class.param_plot_obj.output_dict
        for p in range(len(param_plot)):
            plot_class.__main_plotmap__(param_plot[str(p+1)])
    else:
        raise Exception ("{} not implemented".format(config_class.config["global"]["type_plot"]))
