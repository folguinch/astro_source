import os, argparse
from configparser import ExtendedInterpolation

import numpy as np

from .image import Image

class LoadFITS(argparse.Action):
    """Action class for loading fits files with atroSource Image"""

    def __call__(self, parser, namespace, values, option_string=None):
        images = []
        try:
            if values.lower()=='none':
                setattr(namespace, self.dest, None)
            assert os.path.isfile(values)
            images += [Image(values)]
        except (TypeError,AttributeError):
            for val in values:
                if val.lower()=='none':
                    images += [None]
                else:
                    try:
                        assert os.path.isfile(val)
                    except AssertionError:
                        print('File %s does not exist' % val)
                        exit()
                    images += [Image(val)]
        setattr(namespace, self.dest, images)

