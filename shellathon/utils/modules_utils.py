import importlib
import os


def load_class(class_path):
    module_path, func_name = class_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)


def get_classpath(cls):
    return f'{cls.__module__}.{cls.__name__}'


def get_modulepath(module):
    return f'{module.__package__}.{module.__name__}'


def get_module_fullpath(module):
    return os.path.abspath(module.__file__)

def get_module_dirpath(module):
    return os.path.dirname(get_module_fullpath(module))

def get_module_filename(module):
    return os.path.basename(get_module_fullpath(module))


def get_modulename(module):
    if module.__name__ == '__main__':
        return os.path.splitext(get_module_filename(module))[0]
    return objname(module).rsplit('.',1)[-1]


def classname(ins):
    return ins.__class__.__name__


def objname(obj):
    return obj.__name__
