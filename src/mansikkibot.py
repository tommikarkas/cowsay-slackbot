import os
import time
import re
import wrappers
from slackclient import SlackClient


READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose


class Message():

    """ Slack message """
    def __init__(self, rtm_event):
        self.channel = rtm_event["channel"]
        self.user = rtm_event["user"]
        self.text = rtm_event["text"]


    def __str__(self):
        return self.channel + " " + self.user + " " + self.text


    def sent_at(self, id):
        return "<@" + id + ">" in self.text


    def is_direct(self):
        return self.channel.startswith("D")



class Bot():

    """ Slack bot """
    def __init__(self, bot_name, bot_token):
        self.bot_id = None
        self.bot_name = bot_name
        self.bot_token = bot_token


    def connect(self):
        """Connect to Slack"""
        self.slack_client = SlackClient(self.bot_token)
        if self.slack_client.rtm_connect():
            print("MansikkiBot connected and running!")
            self.bot_id = self._get_id()
        else:
            raise Exception("Connection failed. Invalid Slack token or bot ID?")


    def listen(self):
        """Start listening to events using the real time messaging API"""
        while True:
            rtm_events = self.slack_client.rtm_read()
            messages = self._read_messages(rtm_events)
            self.handle_messages(messages)
            time.sleep(READ_WEBSOCKET_DELAY)


    def say(self, channel, text):
        """Say a message to a channel"""
        self.slack_client.api_call(
          "chat.postMessage", channel=channel,
          text=text, as_user=True)


    def handle_message(self, message):
        """Subclass to implement"""
        print(message)


    def handle_messages(self, messages):
        """Handles a list of messages"""
        for msg in messages:
            # Don't handle own messages
            if (msg.user != self.bot_id):
                self.handle_message(msg)


    def _read_messages(self, rtm_events):
        """Reads the event list and returns any messages"""
        messages = []
        if (rtm_events and len(rtm_events) > 0):
            for rtm_event in rtm_events:
                if "type" in rtm_event and rtm_event["type"] == "message":
                    msg = Message(rtm_event)
                    messages.append(msg)
        return messages


    def _get_id(self):
        """Finds the bot's ID using the API"""
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return user.get("id")
        else:
            raise Exception("Failed to resolve the bot ID")



class MansikkiBot(Bot):

    """ Slack bot """
    def __init__(self, bot_name, bot_token):
        self.bot_name = bot_name
        self.bot_token = bot_token


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
