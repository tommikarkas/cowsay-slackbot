import os
import argparse
import shlex
from slackbot import Bot
from CowfileAction import CowfileAction
from FortuneAction import FortuneAction
from RoutaheAction import RoutaheAction
from wrappers import list_cowfiles, cowsay
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class MansikkiBot(Bot):
    # use argparse for parsing the message
    _parser = argparse.ArgumentParser(description='See documentation for correct arguments',prefix_chars='!')

    def __init__(self, bot_name, bot_token):

        self._parser.add_argument('!cowsay',  action='store_true')
        self._parser.add_argument('!fortune', action=FortuneAction, nargs=0)
        choices = list_cowfiles()
        self._parser.add_argument('!cowfile', action=CowfileAction, nargs=1, choices=choices)
        self._parser.add_argument('!routahe', action=RoutaheAction, nargs=2, metavar=('"From Address"', '"To Address"'))
        self._parser.add_argument('text', nargs='*', help="Message for the cowsay slackbot")
        Bot.__init__(self, bot_name, bot_token)

    # Override
    def handle_message(self, message):
        """Handles a message"""
        print(message)

        args = ''

        # Respond if message is @mansikkibot or on a direct message channel
        if (message.sent_at(self.bot_id) or message.is_direct()):

            # Strip away the at-tag
            text = message.text.replace("<@" + self.bot_id + ">", "")
            try:
                # Parse string with according to shell logic, e.g. substrings are one arg
                args, unknown = self._parser.parse_known_args(shlex.split(text))
                # Cowsay wise things
                print(args)
                if (args.cowsay == True):
                    try:
                        if(args.fortune):
                            cowsay_content = args.fortune
                        elif(args.routahe):
                            cowsay_content = args.routahe
                        elif(args.text):
                            cowsay_content = " ".join(args.text)
                        else:
                            cowsay_content = ''

                        cowsay_text = cowsay(cowsay_content, (args.cowfile if args.cowfile is not None else "default"))
                        self.say(message.channel, "```" + cowsay_text  + "```")
                    except Exception as e:
                        print("ERROR")
                        print(e)
            except:
                print("ERROR: Argument parsing went wrong")

if __name__ == "__main__":
    BOT_NAME = os.environ.get("BOT_NAME")
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

    bot = MansikkiBot(BOT_NAME, SLACK_BOT_TOKEN)
    bot.connect()
    bot.listen()
