import os
from .base import *

if os.environ.get('MODE') == 'prod':
    from .prod import *
else:
    from .dev import *
