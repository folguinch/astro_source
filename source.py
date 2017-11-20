import os, argparse

import astropy.units as u
from astropy.coordinates import SkyCoord
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
    logger = get_logger(__name__)

    def __init__(self, name, config):
        """Creates a new Source.

        Parameters:
            name: the name of the source.
            config: the configuration file.
        """
        # Initialize
        self.logger.info('Initializing source: %s', name)
        super(Source, self).__init__(name, config)

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

    def get_quantity(self, prop, section='INFO'):
        q = self.config.get(section, prop).split()
        return float(q[0]) * u.Unit(q[1])

    @property
    def distance(self):
        return self.get_quantity('distance')

    @property
    def luminosity(self):
        return self.get_quantity('luminosity')

    @property
    def position(self):
        ra = self.config.get('INFO','ra')
        dec = self.config.get('INFO','dec')
        frame = self.config.get('INFO','frame',fallback='icrs')
        return SkyCoord(ra, dec, frame=frame)

    @property
    def ra(self):
        return self.position.ra

    @property
    def dec(self):
        return self.position.dec

    def get_type(self, section):
        """Get the type of data.

        Parameters:
            section (str): the data key.
        """
        assert section in self.config.sections()
        return self.config[section]['type'].lower()

    def load_data(self, section):
        """Load the data.

        It uses the classes registered in *REGISTERED_CLASSES* to identify
        which type of data it has to load. The data information (e.g. file 
        name) has to be source configuration file.

        Parameters:
            section (str): the data to be loaded.
        """
        data_file = os.path.expanduser(self.config[section]['file'])
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
            'config/source.cfg'))
        setattr(namespace, self.dest, source)

