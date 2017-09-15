import os

import numpy as np

from data import Data

class Profile(Data):
    """Creates a radial profile.

    Attributes:
        address: file name
        data: radial profile
        units: units of the elements of the profile
        wlg: wavelength
    """

    def __init__(self, file_name, wlg=None):
        """Creates a new profile object.

        Parameters:
            file_name (str): file name of the profile.
            wlg (float, default=None): wavelength.
        """
        super(Profile, self).__init__(file_name)
        self.wlg = wlg

    def load(self):
        """Load prfile from file.

        Each file has a standard structure with the data in different columns.
        First column for the distance to the peak, second for the flux, third
        for the error. All other columns are ignored.
        """
        self.data, self.units = load_struct_array(self.address)

    def save(self, file_name=None):
        """Save the profile to file.

        Parameters:
            file_name (default=None): new file name.
        """
        save_struct_array(file_name, self.data, self.units)


        
