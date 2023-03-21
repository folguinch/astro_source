"""Data loading functions."""
from typing import Any, Dict

def load_data_by_type(file_name: 'pathlib.Path',
                      dtype: str,
                      loaders: Dict,
                      **kwargs) -> Any:
    """Load the data with the corresponding type from classes.

    Args:
      file_name: data file name.
      dtype: data type.
      classes: dictionary relating each type to an object.
      kwargs: optional; additional arguments for loader function.
    """
    if dtype not in loaders:
        raise TypeError(f'Type {dtype} does not exist')
    return loaders[dtype](file_name, **kwargs)

def kwargs_from_config(config: 'configparseradv.configparser.ConfigParserAdv',
                       base: str = 'loader') -> Dict:
    """Generate a keyword dictionary from options begining with `base`.

    To read a keyword, the option in config must be formatted as:
    `base_keyword`. If an option with the `base_keyword_type` format is
    present, then its value is used to change the the type of the data.
    The default `base` is `loader`.

    Example:

    For `spectral_cube` objects a boolean keyword can be defined to switch off
    the use of dask:
    ```ini
    file: cube_example.fits
    type: spectral_cube
    loader_usedask: false
    loader_usedask_type: bool
    ```
    This will call `SpectralCube('cube_example.fits', usedask=False)`

    Args:
      config: config parser proxy.
      base: optional; look for options that starts with this string.
    """
    kwargs = {}
    for key in config:
        if key.startswith(base) and not key.endswith('type'):
            # Check for type
            if key + '_type' in config:
                dtype = config[key + '_type']
            else:
                dtype = None

            # Split key
            newkey = '_'.join(key.split('_')[1:])

            # Assign value
            if dtype == 'int':
                kwargs[newkey] = config.getint(key)
            elif dtype == 'float':
                kwargs[newkey] = config.getfloat(key)
            elif dtype == 'bool':
                kwargs[newkey] = config.getboolean(key)
            elif dtype == 'quantity':
                kwargs[newkey] = config.getquantity(key)
            else:
                kwargs[newkey] = config[key]

    return kwargs
