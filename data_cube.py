import numpy as np

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

    def spectral_slab(self, rng):
        """Wrap of the ``spectral_cube.spectral_slab`` function."""
        return self.data.spectral_slab(np.min(rng), np.max(rng))
