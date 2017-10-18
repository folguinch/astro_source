import os, argparse

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
        # Initialize
        super(Source, self).__init__(name)

        # Get class logger
        self.logger = get_logger(__name__)
        self.logger.info('Initializing source: %s', self.name)

        # Load configuration
        self.logger.debug('Loading configuration file: %s', config)
        self.load_config(config)
        self.logger.info('Configuration file loaded')

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

class NewSource(argparse.Action):
    """Action class for loading a source in argparse
    """

    def __init__(self, option_strings, dest, nargs=None, const=None, default=None,
            type=None, choices=None, required=False, help=None, metavar=None,
            config=None):
        super(NewSource,self).__init__(option_strings, dest, nargs=None, 
                const=None, default=None, type=None, choices=None, 
                required=False, help=None, metavar=None)
        self.source_dir = config.get('DIRECTORIES', 'sources')
        return

    def __call__(self, parser, namespace, values, option_string=None):
        source = Source(values, os.path.join(self.source_dir, values,
            'config/config.cfg'))
        setattr(namespace, self.dest, source)

