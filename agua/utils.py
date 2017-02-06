import importlib

from comparators import CHECK_FUNCTIONS


def dyn_import(path):
    mods = path.split(".")
    func_name = mods[-1]
    mods = ".".join(mods[:-1])
    return getattr(importlib.import_module(mods), func_name)


def get_check_function(path):
    if path in CHECK_FUNCTIONS:
        return CHECK_FUNCTIONS[path]
    else:
        return dyn_import(path)


def as_percent(n, total):
    return '%.2f' % (float(n) / total * 100)


def label_width(string):
    return "%14s" % (string)
