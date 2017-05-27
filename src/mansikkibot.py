import os
import time
import re
import slackbot
import wrappers
from slackclient import SlackClient


class MansikkiBot(slackbot.Bot):

    def handle_message(self, message):
        """Handles a message"""
        print(message)
        # Respond if message is @mansikkibot or on a direct message channel
        if (message.sent_at(self.bot_id) or message.is_direct()):

            # Strip away the at-tag
            text = message.text.replace("<@" + self.bot_id + ">", "")

            # Check cowfile flag
            cowfile = "default"
            matches = re.search("\\!cowfile\\:([a-z]+)", text)
            if matches:
                cowfile = matches.group(1)
                text = text.replace(matches.group(0), "").strip()
                print("COWFILE: " + matches.group(1))

            # Check for fortune flag
            if text.strip() == "!fortune":
                text = wrappers.fortune()

            # Cowsay
            if (len(text) > 0):
                try:
                    cowsay_text = wrappers.cowsay(text, cowfile)
                    self.say(message.channel, "```" + cowsay_text  + "```")
                except Exception as e:
                    print("ERROR")
                    print(e)



if __name__ == "__main__":
    BOT_NAME = os.environ.get("BOT_NAME")
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

    bot = MansikkiBot(BOT_NAME, SLACK_BOT_TOKEN)
    bot.connect()
    bot.listen()
