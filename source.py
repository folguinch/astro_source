"""Classes for managing and creating astro sources."""
from pathlib import Path
from typing import Optional, Sequence, Union
import argparse

from astropy.coordinates import SkyCoord
from configparseradv import ConfigParserAdv
from toolkit.logger import get_logger

from .container import Container
from .loaders import load_data_by_type, kwargs_from_config
from .register import REGISTERED_CLASSES

class Source(Container):
    """Manages an astronomical source properties and data.

    Attributes:
      name: name of the source.
      config_file: configuration file name.
      config: configuration file of the source.
      log: logging manager.
      _data: the data belonging to the source.
    """
    log = get_logger(__name__, filename=__package__+'.log')

    def __init__(self,
                 name: Optional[str] = None,
                 config_file: Optional[Union[Path, str]] = None,
                 config: Optional[ConfigParserAdv] = None):
        """Creates a new Source.

        Args:
          name: optional; the name of the source.
          config_file: optional; configuration file name.
          config: optional; `ConfigParserAdv` object.
        """
        assert name is not None or config is not None

        # Initialize
        if name is not None:
            self.log.info('Initializing source: %s', name)
        else:
            self.log.info('Initializing source from configuration')
        super().__init__(name, config_file=config_file, config=config)

    def __str__(self):
        """String representation."""
        lines = [f'{self.name}', '-'*len(self.name)]
        for opt, val in self.config.items('INFO'):
            lines.append(f'{opt} = {val}')
        if self._data:
            lines.append('Loaded data:')
            for key in self._data:
                lines.append(f'\t{key}')
        return '\n'.join(lines)

    def get_quantity(self, opt, section='INFO'):
        """Get value in config as quantity."""
        return self.config.getquantity(section, opt, fallback=None)

    @property
    def distance(self):
        return self.get_quantity('distance')

    @property
    def luminosity(self):
        return self.get_quantity('luminosity')

    @property
    def position(self):
        ra = self.config['INFO']['ra']
        dec = self.config['INFO']['dec']
        frame = self.config.get('INFO', 'frame', fallback='icrs')
        return SkyCoord(ra, dec, frame=frame)

    @property
    def ra(self):
        return self.position.ra

    @property
    def dec(self):
        return self.position.dec

    def get_type(self, section: str) -> str:
        """Get the type of data.

        Args:
          section: the data key.
        """
        return self.config[section]['type'].lower()

    def load_data(self, section: str,
                  file_name: Optional[Union[Path, str]] = None,
                  **kwargs) -> None:
        """Load the data.

        It uses the classes registered in `REGISTERED_CLASSES` to identify
        which type of data it has to load. The data information (e.g. file
        name) has to be in the source configuration file.

        Args:
          section: the data section to be loaded.
          file_name: optional; overwrites the config file name.
          kwargs: optional; additional arguments for loader function.
        """
        # File name
        if file_name is not None:
            data_file = Path(file_name).expanduser()
        else:
            data_file = self.config.getpath(section, 'file', fallback=None)
        if data_file is None:
            raise ValueError(f'Could not load data for {section}')

        # Load data
        dtype = self.config[section]['type'].lower()
        kwargs_load = kwargs_from_config(self.config[section])
        kwargs_load.update(kwargs)
        self._data[section] = load_data_by_type(data_file,
                                                dtype,
                                                REGISTERED_CLASSES,
                                                **kwargs_load)

        # Update config
        super().load_data(section, file_name=file_name)

    def load_all_data(self):
        """Load all the data in the configuration file."""
        for section in self.config.sections():
            if section == 'INFO' or 'type' not in self.config[section]:
                continue
            else:
                self.logger.info(f'Loading: {section}')
                self.load_data(section)

    def load_config(self,
                    config_file: Path,
                    update_from: Optional[ConfigParserAdv] = None,
                    default_section: str = 'DEFAULT') -> None:
        """Load a configuration file.

        Args:
            config_file (str): name of the configuration file
        """
        super().load_config(config_file, update_from=update_from,
                            default_section=default_section)

        # Check INFO section
        if 'INFO' not in self.config:
            self.log.warning(('Source does not have INFO section: '
                              'some functions will not work'))

class LoadSource(argparse.Action):
    """Load a source in from config."""

    def __init__(self,
                 option_strings: Sequence[str],
                 dest: str,
                 **kwargs) -> None:
        defaults = {'nargs': 1,
                    'metavar': 'SRC_CONFIG',
                    'help': 'Source configuration file'}
        defaults.update(kwargs)
        super().__init__(option_strings, dest, **defaults)

    def __call__(self, parser, namespace, values, option_string=None):
        source = Source(config_file=values[0].expanduser())
        setattr(namespace, self.dest, source)

class LoadSources(argparse.Action):
    """Load sources from configuration files."""

    def __init__(self,
                 option_strings: Sequence[str],
                 dest: str,
                 **kwargs) -> None:
        defaults = {'nargs': '*',
                    'metavar': ('SRC_CONFIG',),
                    'help': 'Sources configuration files'}
        defaults.update(kwargs)
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, vals, option_string=None):
        sources = [Source(config_file=Path(val).expanduser()) for val in vals]
        setattr(namespace, self.dest, sources)
