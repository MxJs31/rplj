from pathlib import Path
from importlib import import_module
import sys

sys.path.insert(0, __spec__.submodule_search_locations[0])

analyzers = {}

for child in Path(__spec__.submodule_search_locations[0]).iterdir():
    if not child.is_file():
        continue

    if child.suffix != '.py' or child.stem == '__init__':
        continue

    analyzers[child.stem] = import_module(child.stem)

if __spec__.submodule_search_locations[0] in sys.path:
    sys.path.remove(__spec__.submodule_search_locations[0])

del Path, import_module, sys, child