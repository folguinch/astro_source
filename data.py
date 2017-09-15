from abc import ABCMeta, abstractmethod

class Data(object):
    """Data ABC.

    Attributes:
        address: file name
        data: the data in the file
    """

    __metaclass__ = ABCMeta

    def __init__(self, address):
        """Defines a new data object.

        Parameters:
            address: filename
        """
        self.address = address
        self.data = None

        if os.path.isfile(file_name):
            self.load(file_name)

    @abstractmethod
    def load(self):
        """Open file in *address*."""
        pass

    @abstractmethod
    def save(self, address=None):
        """Saves the file in *address* or in a new address if provided.
        
        Parameters:
            address (default=None): new address
        """
        pass
