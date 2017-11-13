from spectral_cube import SpectralCube
from astropy.io import fits
from astropy.wcs import WCS
from myutils.logger import get_logger

from .data import Data

class Data3D(Data):
    """ Creates a data cube structure.

    Attributes:
        address: file name.
        data: the data cube.
    """

    def __init__(self, address):
        """Defines a new data cube object.

        Parameters:
            address (str): file name.
        """
        super(Data3D, self).__init__(address)
        self.logger = get_logger(__name__)

    def load(self):
        """Load the data cube"""
        try:
            self.data = SpectralCube.read(self.address)
        except:
            self.logger.warn('Trying to fix the cube')
            cube = fits.open(fname)[0]
            cube.header['CUNIT3'] = 'm/s'
            cube.header['CRVAL3'] = cube.header['CRVAL3'] * 1.E3
            cube.header['CDELT3'] = cube.header['CDELT3'] * 1.E3
            self.data = SpectralCube(cube.data, WCS(cube.header))
            self.logger.info('Cube fixed')
