"""
Pretend that a package is installed.

Anything can be imported from the specified namespace. Names starting in lower
case are imported as packages (so other names can be imported from them), names
staring in upper case are imported as classes (so they can be used as type
annotations).

The import process in python is documented in https://docs.python.org/3/library/importlib.html

In short, when importing a module, python goes through the finder objects in
``sys.meta_path`` until the ``find_spec`` method of one of them returns a
module specification for the module name requested. That specification
contains the name of the module, the loader class that will deal with creating
the module object, and if the module is a package (from which other modules can
be imported).

>>> from pretends import add_pretend_module
>>> add_pretend_module('do_not_exist')
>>> from do_not_exist.really.fictive import DummyTypeHint
"""

import sys
from importlib.abc import MetaPathFinder, Loader
from importlib.machinery import ModuleSpec
from types import ModuleType


class PretendModule(ModuleType):
    def __getattr__(self, name):
        if name[0].isupper():
            return type(name, (object, ), {})
        raise AttributeError


class PretendFinder(MetaPathFinder):
    def __init__(self, module_root_name):
        self.module_root_tokens = module_root_name.split('.')
    
    def is_pretend_package(self, fullname):
        name_tokens = fullname.split('.')
        name = name_tokens[-1]
        root_length = len(self.module_root_tokens)
        return (
            len(name_tokens) > root_length
            and name_tokens[:root_length] == self.module_root_tokens
            and name[0] and name[0].isupper
        )

    def find_spec(self, fullname, path, target=None):
        if self.is_pretend_package(fullname):
            return build_pretend_spec(fullname)
        return None


class PretendLoader(Loader):
    @staticmethod
    def create_module(spec: ModuleSpec) -> ModuleType:
        name = spec.name
        module = PretendModule(name)
        module.__package__ = name
        return module
    
    @staticmethod
    def exec_module(module):
        pass
    

def build_pretend_spec(fullname):
    return ModuleSpec(fullname, PretendLoader, is_package=True)


def add_pretend_module(fullname):
    finder = PretendFinder(fullname)
    sys.meta_path.append(finder)