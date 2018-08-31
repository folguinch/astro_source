import os
from abc import ABCMeta, abstractmethod
from configparser import ExtendedInterpolation

from myutils.logger import get_logger
from myutils.myconfigparser import myConfigParser

class Container(object):
    """Defines a container ABC.

    Attributes:
        name: name of the container
        config: configuration 
        data: all the data contained
    """
    __metaclass__ = ABCMeta
    logger = get_logger(__name__)

    def __init__(self, name, config=None):
        """Defines a new container.

        Parameters:
            name: container name
        """
        self.name = name
        self.data = {}

        if config:
            # Load configuration
            self.logger.debug('Loading configuration file: %s', config)
            try:
                assert os.path.isfile(config)
            except AssertionError:
                self.logger.exception('File %s does not exist', config)
                exit()
            self.load_config(config)
            self.logger.info('Configuration file loaded')
        else:
            self.config = None

    @abstractmethod
    def load_data(self, key, file_name):
        """Load *data* from file and save it in *key*"""
        pass

    def __getitem__(self, key):
        assert key in self.data.keys()
        return self.data[key]

    def __setitem__(self, key, value):
        self[key] = value

    def load_data_from_keys(self, keys, file_names):
        """Load all the data in each file in *file_names* and store it in
        *key*
        
        Parameters:
            keys (iterable): list of keys for each file
            file_names (iterable): list of files to load
        """
        for k,f in zip(keys, file_names):
            self.load_data(k, f)

    def load_config(self, config_file):
        """Load a configuration file.

        Parameters:
            config_file (str): name of the configuration file
        """
        self.config = myConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(config_file)

