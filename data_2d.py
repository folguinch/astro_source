from data import Data

from astropy.io import fits

class Data2D(Data):
    """Defines a data in 2D.

    Can be used for loading images or visibility maps.
    
    Attributes:
        address: file name.
        data: the data.
        nhdu: HDU number to work with.
    """

    def __init__(self, address):
        """Defines a new data object.

        Parameters:
            address: filename
        """
        super(Data2D, self).__init__(address)
        self.nhdu = 0

    def load(self):
        """Load the data"""
        self.data = fits.open(self.address)

    def save(self, file_name=None):
        """Save the data.

        Parameters:
            file_name (default=None): new file name.
        """
        self.data.writeto(file_name or self.address , clobber=True)
