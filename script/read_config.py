import configparser

import configparser
import datetime

class Config:
    def __init__(self, config_opts):
        """
        Initialise la configuration à partir d'un fichier et génère une liste de dates.

        :param config_opts: Objet contenant les options de configuration (cfg, start, end, listdate, deltat).
        :raises Exception: Si le fichier de configuration ou les paramètres nécessaires sont absents.
        """
        if not config_opts.cfg:
            raise Exception("The config file is absent.")
        
        self.config = configparser.ConfigParser()
        self.config.read(config_opts.cfg)
        self.create_listdate(config_opts)

    def create_listdate(self, config_opts):
        """
        Crée une liste de dates en fonction des options de configuration.

        :param config_opts: Objet contenant les paramètres (start, end, listdate, deltat).
        :raises Exception: Si les paramètres de date sont incomplets ou mal formatés.
        """
        if not config_opts.listdate and (not config_opts.start or not config_opts.end):
            raise Exception("Both start/end and listdate cannot be None simultaneously.")
        
        if config_opts.listdate:
            # Si listdate est fournie, découpe en une liste.
            self.listdate = config_opts.listdate.split(',')
        else:
            # Valide le format des dates de début et de fin.
            if len(config_opts.start) != 10 or len(config_opts.end) != 10:
                raise Exception("Start and end must be in the format 'YYYYMMDDHH'.")
            
            # Convertit start et end en objets datetime.
            try:
                start = datetime.datetime.strptime(config_opts.start, "%Y%m%d%H")
                end = datetime.datetime.strptime(config_opts.end, "%Y%m%d%H")
            except ValueError:
                raise Exception("Invalid date format for start or end.")

            # Définit le pas de temps (deltat) en heures, valeur par défaut = 1 heure.
            deltat = int(config_opts.deltat) if config_opts.deltat else 1

            # Génère les dates avec un intervalle de `deltat` heures.
            self.listdate = []
            while start <= end:
                self.listdate.append(start.strftime("%Y%m%d%H"))
                start += datetime.timedelta(hours=deltat)


    
