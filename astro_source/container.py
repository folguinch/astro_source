"""Container classes."""
from pathlib import Path
from typing import Any, Sequence, Optional, Union
import abc

from configparseradv.configparser import ConfigParserAdv
from toolkit.logger import get_logger

class Container(metaclass=abc.ABCMeta):
    """Creates a container abstract class.

    Abstract methods to implement:

    - `load_data`

    Attributes:
      name: name of the container.
      config_file: configuration file name.
      config: configuration.
      log: logging system.
      _data: open the data as required.
    """
    log = get_logger(__name__, filename=__package__+'.log')

    def __init__(self,
                 name: Optional[str] = None,
                 config_file: Optional[Union[Path, str]] = None,
                 config: Optional[ConfigParserAdv] = None,
                 default_section: str = 'DEFAULT'):
        """Initializes a new container.

        Args:
          name: container name.
          config_file: optional; configuration file name.
          config: optional; `ConfigParserAdv` object.
        """
        # Store name
        self.name = name
        self._data = {}

        if config_file is not None:
            self.config_file = Path(config_file).expanduser()

            # Load configuration
            if self.config_file.is_file():
                self.log.info('Loading config file: %s', self.config_file)
                self.load_config(config_file, update_from=config,
                                 default_section=default_section)
                self.log.debug('Configuration file loaded')
            else:
                self.config = ConfigParserAdv(default_section=default_section)

            # Update name
            if name is None and 'name' in self.config[default_section]:
                self.name = self.config[default_section]['name']
            elif name is not None:
                self.config[default_section]['name'] = name
            else:
                self.log.warning('Could not determine name')
        elif config is not None:
            self.config = config
            self.log.info('Configuration assigned')

            # Update name
            if name is None and 'name' in config[default_section]:
                self.name = config[default_section]['name']
                self.config_file = Path(f'{name}.cfg')
            elif name is not None:
                self.config_file = Path(f'{name}.cfg')
                self.config[default_section]['name'] = name
            else:
                self.log.warning('Could not determine name and config file')
        else:
            self.config = ConfigParserAdv(default_section=default_section)

            # Update name
            if name is None:
                self.log.warning('Could not determine config file name')
                self.config_file = None
            else:
                self.config_file = Path(f'{name}.cfg')

    @abc.abstractmethod
    def load_data(self,
                  section: str,
                  file_name: Optional[Path] = None):
        """Load data from file or config section and store it."""
        if file_name is not None:
            self.update_config(section, file=str(file_name))

    def update_config(self, section: str, **kwargs):
        """Update config `section` with options and values in `kwargs`"""
        if section not in self.config:
            self.log.info('Adding section %s', section)
            new_vals = {f'{key}': f'{val}' for key, vals in kwargs.items()}
            self.config[section] = new_vals
        else:
            self.log.info('Updating section %s', section)
            for key, val in kwargs.items():
                self.config[section][key] = str(val)

    def copy_config(self, section: str, new_section: str):
        """Copy config section ignoring defaults."""
        self.config.copy_section(section, new_section, ignore_default=True)

    def __getitem__(self, section: str):
        if section not in self._data:
            self.load_data(section)
        return self._data[section]

    def __setitem__(self, section: str, value: Any):
        self[section] = value

    def load_data_from_keys(self,
                            sections: Sequence[str],
                            file_names: Sequence[Path]) -> None:
        """Load all the data in each file and store.

        The `sections` and `file_names` are inserted/updated in the
        configuration attribute.

        Args:
          sections: list of sections for each file.
          file_names: list of files to load.
        """
        for section, fname in zip(sections, file_names):
            self.load_data(section, fname)

    def load_config(self,
                    config_file: Path,
                    update_from: Optional[ConfigParserAdv] = None,
                    default_section: str = 'DEFAULT') -> None:
        """Load a configuration file.

        If `update_from` is given, the configuration values are updated from
        this parser.

        Args:
          config_file: file name of the configuration file.
          update_from: optional; `ConfigParserAdv` like object to update
            values in file.
          default_section: optional; default section for parser.
        """
        self.config = ConfigParserAdv(default_section=default_section)
        self.config.read(config_file)
        if update_from is not None:
            self.config.read_dict(update_from)

    def write(self, filename: Optional[Path] = None) -> None:
        """Write configuration file to disk."""
        if filename is None and self.config_file is not None:
            filename = self.config_file
        elif filename is None and self.config_file is None:
            raise ValueError('Source does not have config file')
        else:
            pass

        with filename.open('w', encoding='utf-8') as fl:
            self.config.write(fl)

    def get_data_sections(self, dtypes: Sequence) -> Sequence:
        """Return the sections in configuration that have data."""
        sections = []
        for section, cfg in self.config.items():
            if 'type' not in cfg:
                continue
            elif cfg['type'] in dtypes:
                sections.append(section)

        return sections

