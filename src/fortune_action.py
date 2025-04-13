from argparse import Action

from src.wrappers import fortune


class FortuneAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        text = fortune()
        setattr(namespace, self.dest, text)
