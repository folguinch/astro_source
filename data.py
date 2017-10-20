import os
from abc import ABCMeta, abstractmethod
from myutils.logger import get_logger

class Data(object):
    """Data ABC.

    Attributes:
        address: file name.
        data: the data in the file.
        logger: logging manager.
    """

    __metaclass__ = ABCMeta

    def __init__(self, address=None, data=None):
        """Defines a new data object.

        Parameters:
            address: filename
        """
        self.address = address
        self.data = data
        self.logger = get_logger(__name__)

        if address and os.path.isfile(address):
            self.logger.debug('Load file: %s', address)
            self.load()

    @abstractmethod
    def load(self):
        """Open file in *address*."""
        pass

    @abstractmethod
    def save(self, file_name=None):
        """Saves the file in *address* or in a new address if provided.
        
        Parameters:
            file_name (default=None): new file name.
        """
        pass
