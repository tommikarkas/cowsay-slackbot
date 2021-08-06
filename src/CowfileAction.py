import argparse


class CowfileAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        # Check cowfile flag

        _cowfile = values[0].strip()
        print("COWFILE changed: " + _cowfile)

        setattr(namespace, self.dest, _cowfile)
