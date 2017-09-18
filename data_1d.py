from myutils.array_utils import *

from data import Data

class Data1D(Data):
    """Creates a 1-D data structure.

    This object is useful to managa data like radial profiles, spectra or
    slices.

    Attributes:
        address: file name
        data: the data
        units: units of the elements of the data
    """

    def __init__(self, file_name, wlg=None):
        """Creates a new profile object.

        Parameters:
            file_name (str): file name of the profile.
            wlg (float, default=None): wavelength.
        """
        self.units = None
        super(Profile, self).__init__(file_name)

    def load(self):
        """Load data from file.

        Each file has a standard structure with the data in different columns.
        """
        self.data, self.units = load_struct_array(self.address)

    def save(self, file_name=None):
        """Save the data to file.

        Parameters:
            file_name (default=None): new file name.
        """
        save_struct_array(file_name, self.data, self.units)

    def convert(self, key, new_unit):
        """Convert the units of data in *key* to *new_unit*.

        Parameters:
            key (str): data to convert.
            new_unit (astropy.unit): new physical unit.
        """
        self.data[key] = (self.data[key]*self.units[key]).to(new_unit).value
        self.units[key] = 1.*new_unit
