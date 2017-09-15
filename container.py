from abc import ABCMeta, abstractmethod
from configparser import ConfigParser, ExtendedInterpolation

class container(object):
    """Defines a container ABC.

    Attributes:
        name: name of the container
        config: configuration 
        data: all the data contained
    """

    __metaclass__ = ABCMeta

    def __init__(self, name):
        """Defines a new container.

        Parameters:
            name: container name
        """
        self.name = name
        self.config = None
        self.data= {}

    @abstractmethod
    def load(self, key, file_name):
        """Load *data* from file and save it in *key*"""
        pass

    def load_all(self, keys, file_names):
        """Load all the data in each file in *file_names* and store it in
        *key*
        
        Parameters:
            keys (iterable): list of keys for each file
            file_names (iterable): list of files to load
        """
        for k,f in zip(keys, file_names):
            self.load(k, f)

    def load_config(self, config_file):
        """Load a configuration file.

        Parameters:
            config_file (str): name of the configuration file
        """
        self.config = ConfigParser(interpolation=ExtendedInterpolation)
        self.config.read(config_file)


