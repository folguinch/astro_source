from astropy.io import fits
import astropy.units as u
from myutils.logger import get_logger

from .data import Data

class Data2D(Data):
    """Defines a data in 2D.

    Can be used for loading images or visibility maps.
    
    Attributes:
        address: file name.
        data: the data.
        nhdu: HDU number to work with.
    """

    def __init__(self, address, nhdu=0):
        """Defines a new data object.

        Parameters:
            address (str): file name.
            nhdu (int, default=0): HDU number.
        """
        super(Data2D, self).__init__(address)
        self.nhdu = nhdu
        self.logger = get_logger(__name__)

    def load(self):
        """Load the data"""
        self.data = fits.open(self.address)

    def save(self, file_name=None):
        """Save the data.

        Parameters:
            file_name (default=None): new file name.
        """
        self.data.writeto(file_name or self.address , clobber=True)

    @property
    def array(self):
        return self.data[self.nhdu].data

    @property
    def header(self):
        return self.data[self.nhdu].header

    @property
    def unit(self):
        return 1.*u.Unit(self.header['BUNIT'])
