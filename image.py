from data_2d import Data2D

from astropy.wcs import WCS

class Image(Data2D):
    """Defines an image object.

    Attributes:
        address: file name.
        data: the data.
        nhdu: HDU number to work with.
    """

    @property
    def wcs(self):
        return WCS(self.header)
