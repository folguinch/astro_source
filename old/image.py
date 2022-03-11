from astropy.wcs import WCS
from myutils.logger import get_logger
from myutils.classes.data_2d import Data2D

from .register import register_class

@register_class
class Image(Data2D):
    """Defines an image object.

    Attributes:
        address: file name.
        data: the data.
        nhdu: HDU number to work with.
        logger: logging manager
    """
    logger = get_logger(__name__, __package__+'.log')

    @property
    def wcs(self):
        return WCS(self.header).sub(['longitude', 'latitude'])
