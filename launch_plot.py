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
from read_config import Config
from plot import Plot
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
    # Vérifie si 'Netcdf' doit être ajouté au PYTHONPATH
    for plot in config_class.config["global"]["plot_list"].split(","):
        if "exp" in config_class.config[plot].get('listexp', ''):
            netcdf_path = os.path.abspath("script/Netcdf")
            if netcdf_path not in sys.path:
                print("Ajout du répertoire 'Netcdf' au PYTHONPATH")
                sys.path.append(netcdf_path)
                # Import conditionnel du module
                from read_mocage import Netcdf_mocage

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

    # Initialise la classe Plot
    try:
        plot_class = Plot(config_class)
    except Exception as e:
        print(f"Erreur lors de l'initialisation de Plot : {e}")
        sys.exit(1)
