import os

from myutils.data import load_data_by_type
from myutils.logger import get_logger

from .container import Container
from .register import REGISTERED_CLASSES

class Source(Container):
    """Defines an astronomical source, its properties and data.

    Attributes:
        name: name of the source.
        config: configuration file of the source.
        data: the data belonging to the source.
        logger: logging manager.
    """

    def __init__(self, name, config):
        """Creates a new Source.

        Parameters:
            name: the name of the source.
            config: the configuration file.
        """
        super(Source, self).__init__(name)
        self.load_config(config)
        self.logger = get_logger(__name__)

    def load_data(self, section):
        """Load the data.

        It uses the classes registered in *REGISTERED_CLASSES* to identify
        which type of data it has to load. The data information (e.g. file 
        name) has to be source configuration file.

        Parameters:
            section (str): the data to be loaded.
        """
        assert os.path.isfile(self.config[section]['loc'])

        self.data[section] = load_data_by_type(self.config[section]['loc'], 
                self.config[section]['type'].lower(), REGISTERD_CLASSES)

    def load_all_data(self):
        """Load all the data with information in the configuration file."""
        for section in self.config.sections():
            if section=='INFO' or 'type' not in self.config.options(section):
                continue
            else:
                self.load_data(section)
