"""A package for source information management.


"""
from pathlib import Path

from .register import REGISTERED_CLASSES

# Load all the classes
cwd = Path(__file__).parent
for x in cwd.glob('*.py'):
    if not x.name.startswith('__'):
        __import__(x.stem, globals(), locals())

__all__ = ['REGISTERED_CLASSES']
