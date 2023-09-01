## logger.py is a concrete class that implements the logging.py module for use throughout the program

import logging

## <---------- find way to inherit from logging.log()?
class Log:
    def __init__(self):
        pass

    def create_logger(self, log_name, level='DEBUG'):
        """ creates and returns a logger instance. Creates a file as well as logging output to
        the console.
        
        Keyword arguments:
        log_name -- the name of the log to create
        level -- set the level of severity to log to console. Note that severity level for the log
                file itself is always set to 'DEBUG'
                Possible values are: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        """ 
        formatter = logging.Formatter('%(asctime)s %(levelname)s: (%(module)s.%(funcName)s) %(message)s')
        
        log = logging.getLogger(log_name)
        log.setLevel(logging.DEBUG)
        
        # # create directory/file in lab directory if non-existant ## <------- should be connected to librarian.py
        # directory = ('%s\\%s\\' % (LOG_DIRECTORY, self.name))
        # if not os.path.isdir(directory):
        #     os.makedirs(directory)
        # handler_file_name = ('%s_%s.log' % (self.name, time.strftime("%Y%m%d%H%M%S")))
        
        # create logging file handler
        handler_file = logging.FileHandler('%s\\%s' % (directory, handler_file_name))
        handler_file.setFormatter(formatter)
        handler_file.setLevel(logging.DEBUG)
        log.addHandler(handler_file)
        
        # create console logger. This can have a higher logging level
        console = logging.StreamHandler()
        console.setLevel(eval('logging.' + level))
        console.setFormatter(formatter)
        log.addHandler(console)
        
        log.info('Log file created: ' + str(directory) + str(handler_file_name))
        return log