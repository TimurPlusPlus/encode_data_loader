import log

import resources.configs.test_config as conf


class StreamToLogger(object):
   """
   Fake file-like stream object that redirects writes to a logger instance.
   """
   def __init__(self, logger, log_level=log.DEBUG):
      self.logger = logger
      self.log_level = log_level
      self.linebuf = ''

   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())

log.basicConfig(
    filename=conf.log_file,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log.DEBUG
)
