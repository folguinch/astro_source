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
        try:
            assert os.path.isfile(config)
        except AssertionError:
            self.logger.exception('File %s does not exist', config)
        self.load_config(config)
        self.logger.info('Configuration file loaded')

        # Load data
        self.logger.info('Loading data')
        self.load_all_data()

    def __str__(self):
        """String representation"""
        line = '%s\n%s\n' % (self.name, '-'*len(self.name))
        fmt = '%s = %s\n'
        for item in self.config.items('INFO'):
            line += fmt % item
        if self.data:
            line += 'Loaded data:\n\t'
            for key in self.data.iterkeys():
                line += '%s, ' % key
        return line.strip().strip(',')

    def load_data(self, section):
        """Load the data.

        It uses the classes registered in *REGISTERED_CLASSES* to identify
        which type of data it has to load. The data information (e.g. file 
        name) has to be source configuration file.

        Parameters:
            section (str): the data to be loaded.
        """
        data_file = os.path.expanduser(self.config[section]['loc'])
        assert os.path.isfile(data_file)

        self.data[section] = load_data_by_type(data_file, 
                self.config[section]['type'].lower(), REGISTERED_CLASSES)

    def load_all_data(self):
        """Load all the data with information in the configuration file."""
        for section in self.config.sections():
            if section=='INFO' or 'type' not in self.config.options(section):
                continue
            else:
                self.logger.info('Loading: %s', section)
                self.load_data(section)

class LoadSource(argparse.Action):
    """Action class for loading a source in argparse
    """

    def __init__(self, option_strings, dest, nargs=None, const=None, default=None,
            type=None, choices=None, required=False, help=None, metavar=None,
            source_dir='./'):
        super(LoadSource,self).__init__(option_strings, dest, nargs=nargs, 
                const=const, default=default, type=type, choices=choices, 
                required=required, help=help, metavar=metavar)
        self.directory = os.path.expanduser(source_dir)
        return

    def __call__(self, parser, namespace, values, option_string=None):
        source = Source(values, os.path.join(self.directory, values,
            'config/config.cfg'))
        setattr(namespace, self.dest, source)

