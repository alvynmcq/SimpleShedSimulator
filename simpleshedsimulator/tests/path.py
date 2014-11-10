import os
import sys

if os.name == 'nt':
        path_to_core = "\\".join(sys.path[0].split('\\')[:-1]) + "\\core"
        sys.path.insert(0, path_to_core)
elif os.name == 'possix':
        path_to_core = "//".join(sys.path[0].split('//')[:-1]) + "//core"
        sys.path.insert(0, path_to_core)



