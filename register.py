"""Register classes to open data.

The `REGISTERED_CLASSES` dictionary stores functions/classes to open data.

From:
http://scottlobdell.me/2015/08/using-decorators-python-automatic-registration/
"""
from spectral_cube import SpectralCube
from astropy.io import fits

# Global values
REGISTERED_CLASSES = {
    'spectral_cube': SpectralCube,
    'fits_file': fits.open,
}

def register_class(cls):
    """Register class decorator."""
    REGISTERED_CLASSES[cls.__name__.lower()] = cls
    return cls
