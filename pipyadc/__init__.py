from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .pipyadc import ADS1256
from .pipyadc import ADS79XX