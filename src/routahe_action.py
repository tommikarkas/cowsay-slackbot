import argparse

from src.wrappers import routahe


class RoutaheAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(values)
        routaheResponse = routahe(values[0], values[1])
        setattr(namespace, self.dest, routaheResponse)
