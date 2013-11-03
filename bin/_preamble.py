__metaclass__ = type

__all__ = []

import os
import sys


path = os.path.dirname(os.path.abspath(sys.argv[0]))
while os.path.dirname(path) != path:
    if os.path.exists(os.path.join(path, "jiraban", "__init__.py")):
        sys.path.insert(0, path)
        break
    path = os.path.dirname(path)
