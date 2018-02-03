from myutils.classes.data_1d import Data1D

from .register import register_class

@register_class
class SED(Data1D):
    """Class for managing SEDs.

    Attributes:
        address: file name.
        data: the data.
        units: data units.
        logger: logging manager.
    """
    def interpolate(self, newx, **kwargs):
        return super(SED, self).interpolate('wlg', 'F', newx, **kwargs)
