import configparser

class config:

  def __init__(self, config_opts):
    if config_opts.cfg is None:
      raise Exception("The config file is absent")
    self.config = configparser.ConfigParser()
    self.config.read(config_opts.cfg)  
    self.create_listdate(config_opts)
    
  def create_listdate(self, config_opts):
    if ( config_opts.start is None or config_opts.end is None ) and config_opts.listdate is None:
      raise Exception("Start or end is/are None and listdate is None")
    if config_opts.listdate is not None:
      self.listdate = config_opts.listdate.split(',')
    else:
      if len(config_opts.start) != 10 or len(config_opts.end) != 10:
        raise Exeption("Start and end must be 'YYYYMMDDHH'")
      import datetime
      start = datetime.datetime(int(config_opts.start[:4]),
                                int(config_opts.start[4:6]),
                                int(config_opts.start[6:8]),
                                int(config_opts.start[8:]),
                                0,
                                0)
      end = datetime.datetime(int(config_opts.end[:4]),
                              int(config_opts.end[4:6]),
                              int(config_opts.end[6:8]),
                              int(config_opts.end[8:]),
                              59,
                              59)
      if config_opts.deltat is None:
        deltat = 1
      else:
        deltat = int(config_opts.deltat)
      self.listdate = []
      while start <= end:
        self.listdate.append(start.strftime("%Y%m%d%H"))
        start = start + datetime.timedelta(hours=deltat)
    
