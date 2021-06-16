
import importlib.machinery
import os
import sys

from . import methods


TOP_LEVEL_NAME = os.path.splitext(os.path.basename(sys.argv[1]))[0]
NAMES = {key: vars(methods)[key] for key in vars(methods).keys()
         if not key.startswith('_')}


class Finder(importlib.machinery.PathFinder):
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        spec = super().find_spec(fullname, path, target)
        if spec:
            if isinstance(spec.loader, importlib.machinery.SourceFileLoader):
                spec.loader = Loader(spec.loader.name, spec.loader.path)
        return spec


class Loader(importlib.machinery.SourceFileLoader):
    def exec_module(self, module):
        code = self.get_code(module.__name__)
        if code is None:
            raise ImportError('cannot load module {} when get_code() '
                              'returns None'.format(module.__name__))
        vars(module).update(NAMES)
        if module.__name__ == TOP_LEVEL_NAME:
            module.__name__ = '__main__'
        exec(code, module.__dict__)
