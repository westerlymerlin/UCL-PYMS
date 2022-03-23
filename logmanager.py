import os.path
from settings import settings, version
import logging
from logging.handlers import RotatingFileHandler
import sys


class StdReDirector:
    def __init__(self):
        self.data = []

    def write(self, s):
        if len(s) > 1:
            logger.info(s)

    def flush(self):
        pass


if os.path.isdir(settings['logging']['logfilepath']) is False:
    os.mkdir(settings['logging']['logfilepath'])
logger = logging.getLogger(settings['logging']['logappname'])
logger.setLevel(logging.INFO)
logfilename = '%s%s.log' % (settings['logging']['logfilepath'], settings['logging']['logappname'])
LogFile = RotatingFileHandler(logfilename, maxBytes=1048576, backupCount=10)
formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s : %(message)s')
LogFile.setFormatter(formatter)
logger.addHandler(LogFile)
LogFile.doRollover()
sys.stdout = x = StdReDirector()
print("********************** Starting PyMs Version %s ***********************" % version)
