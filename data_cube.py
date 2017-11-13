from .data_3d import Data3D
from .register import register_class

@register_class
class Cube(Data3D):
    """Class for managing data cubes.

    Attributes:
        address: file name.
        data: the data cube.
        logger: logging manager.
    """

    pass
