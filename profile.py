from myutils.array_utils import *
from myutils.logger import get_logger

from .data_1d import Data1D
from .register import register_class

@register_class
class Profile(Data1D):
    """Creates a radial profile.

    Attributes:
        address: file name
        data: radial profile
        units: units of the elements of the profile
        wlg: wavelength
        logger: logging manager.
    """

    def __init__(self, file_name, wlg=None):
        """Creates a new profile object.

        Parameters:
            file_name (str): file name of the profile.
            wlg (float, default=None): wavelength.
        """
        self.wlg = wlg
        super(Profile, self).__init__(file_name)
        self.logger = get_logger(__name__)

