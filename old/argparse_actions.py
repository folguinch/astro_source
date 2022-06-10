import os, argparse

from .image import Image
from .data_cube import Cube

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

class LoadCube(argparse.Action):
    """Action class for loading fits files with atroSource Image"""

    def __init__(self, option_strings, dest, nargs=None, **kwargs):

        if nargs is not None and nargs>1:
            raise ValueError("only nargs=1 allowed")
        super(LoadCube, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        if len(values)==1 and not hasattr(values, 'lower'):
            fname = values[0]
        else:
            fname = values

        fname = os.path.expanduser(fname)
        cube = Cube(fname)

        setattr(namespace, self.dest, cube)

