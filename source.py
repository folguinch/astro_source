"""Classes for managing and creating astro sources."""
from pathlib import Path
from typing import Optional, Sequence, Union
import argparse

from astropy.coordinates import SkyCoord
from configparseradv.configparser import ConfigParserAdv
from toolkit.logger import get_logger
import astropy.units as u

from .container import Container
from .loaders import load_data_by_type, kwargs_from_config
from .register import REGISTERED_CLASSES

class Source(Container):
    """Manages an astronomical source/region properties and data.

    Attributes:
      name: name of the source.
      config_file: configuration file name.
      config: configuration file of the source.
      subsources: region subsources (if any).
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
        # Initialize
        if name is not None:
            self.log.info('Initializing source: %s', name)
        else:
            self.log.info('Initializing source from configuration')
        super().__init__(name, config_file=config_file, config=config,
                         default_section='DEFAULT')

        # Initiate subsources
        self.subsources = {}
        self.load_subsources()

    def __str__(self):
        """String representation."""
        lines = [f'{self.name}', '-'*len(self.name)]
        for opt, val in self.config.items('INFO'):
            lines.append(f'{opt} = {val}')
        if self.subsources:
            lines.append('Subsources:')
            lines.append(','.join(f' {val.name} (key)'
                                  for key, val in self.subsources.items()))
        if self._data:
            lines.append('Loaded data:')
            for key in self._data:
                lines.append(f'\t{key}')
        lines.append('-'*len(self.name))
        return '\n'.join(lines)

    @classmethod
    def from_values(cls, name: str, **kwargs):
        """Generates a new instance storing the input arguments."""
        # Store values
        config = ConfigParserAdv()
        config.read_dict({'INFO': {'name': name}})
        for key, val in kwargs.items():
            if hasattr(val, 'unit'):
                unit = f'{val.unit}'.replace(' ', '')
                config['INFO'][key] = f'{val.value} {unit}'
            else:
                config['INFO'][key] = f'{val}'

        return cls(config=config)

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
    def vlsr(self):
        return self.get_quantity('vlsr')

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

    def load_subsources(self) -> None:
        """Load the subsources in `Source` configuration."""
        for section, conf in self.config.items():
            if not conf.get('type', fallback='') == 'subsource':
                continue

            self.subsources[section] = SubSource.from_config_proxy(conf,
                                                                   name=section)

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
            elif self.config[section]['type'] == 'subsource':
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

    def write(self, filename: Optional[Path] = None) -> None:
        """Write configuration file to disk."""
        # Store subsources in config
        if self.subsources:
            for key, val in self.subsources.items():
                if key not in self.config:
                    self.config[key] = val.to_dict()

        # Write
        super().write(filename=filename)

    def get_data_sections(self) -> Sequence:
        return super().get_data_sections(tuple(REGISTERED_CLASSES.keys()))

class SubSource(object):
    """Class for storing individual source information.

    Some types of information have default types:

    - `ra`, `dec` and `frame` are stored as `SkyCoord`.
    - `radius` is stored as `astropy.units.Quantity`.

    If only `ra` and `dec` are given, then ICRS is assumed as `frame`.

    Attributes:
      name: subsource name.
      info: source information.
    """

    def __init__(self, name: str, **info):
        self.name = name
        self.info = info

    @classmethod
    def from_config_proxy(cls,
                          parser: ConfigParserAdv,
                          name: Optional[str] = None):
        """Create a new subsource from a `ConfigParser` proxy.

        Args:
          parser: configuration parser proxy.
          name: optional; subsource name.
        """
        name = parser.get('name', fallback=name)

        return cls.from_dict(parser, name=name)

    @classmethod
    def from_dict(cls,
                  data: dict,
                  name: Optional[str] = None):
        """Create a new subsource from a dictionary.

        Args:
          data: configuration parser proxy.
          name: optional; subsource name.
        """
        if name is None:
            name = data.pop('name', name)
        ignore_keys = ['type']
        info = {}
        position = {'frame': 'icrs'}
        for key, val in data.items():
            if key in ignore_keys:
                continue
            elif key in ['ra', 'dec', 'frame']:
                position[key] = val
            elif key in ['radius']:
                info[key] = u.Quantity(val)
            else:
                info[key] = val

        if 'ra' in position and 'dec' in position:
            info['position'] = SkyCoord(**position)

        return cls(name, **info)

    @property
    def position(self):
        """Position of the subsource."""
        return self.info.get('position')

    def to_dict(self) -> dict:
        """Convert the values back to a dictionary with string values."""
        props = {'name': self.name, 'type': 'subsource'}
        for key, val in self.info.items():
            if key == 'position':
                props['ra'], props['dec'] = val.to_string('hmsdms').split()
                props['frame'] = val.frame.name
            elif hasattr(val, 'unit'):
                props[key] = f'{val.value} {val.unit}'
            else:
                props[key] = val

        return props

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
                    'metavar': ('SRC_CONFIG', 'SRC_CONFIG'),
                    'help': 'Sources configuration files'}
        defaults.update(kwargs)
        super().__init__(option_strings, dest, **defaults)

    def __call__(self, parser, namespace, vals, option_string=None):
        sources = [Source(config_file=Path(val).expanduser()) for val in vals]
        setattr(namespace, self.dest, sources)
