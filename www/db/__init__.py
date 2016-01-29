import glob
import importlib
import os.path
import sys

__all__ = []

def load():
    module_paths = glob.glob(os.path.dirname(__file__) + '/*.py')
    module_names = [os.path.basename(f)[:-3] for f in module_paths if os.path.isfile(f)]
    module_names = [m for m in module_names if not m.startswith('_')]

    this_module = sys.modules[__name__]
    for module_name in module_names:
        module = importlib.import_module(__name__ + "." + module_name)
        components = module_name.split('_')
        class_name = "".join(x.title() for x in components)
        setattr(this_module, class_name, getattr(module, class_name))

load()
del load
