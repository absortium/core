import os
import sys

__author__ = 'andrew.shvv@gmail.com'


def reverse_dict(d):
    return {value: key for key, value in d.items()}


def get_attr_from_module(module_name, attr_name):
    return getattr(sys.modules[module_name], attr_name)


def load_environments(module_name, environments):
    settings_module = sys.modules[module_name]
    for elem in environments:
        name = elem[0]
        env_name = elem[1]

        try:
            required = elem[2]
        except IndexError:
            required = None

        value = os.environ[env_name] if env_name in os.environ else None

        if required and value is None:
            raise NotImplementedError("Specify the '{}' environment variable.".format(env_name))
        else:
            setattr(settings_module, name, value)


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
