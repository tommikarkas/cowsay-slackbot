import time
from slackclient import SlackClient


class Message():
    """ Slack message """

    def __init__(self, rtm_event):
        self.channel = rtm_event["channel"]
        self.user = rtm_event["user"]
        self.text = rtm_event["text"]


    def __str__(self):
        return self.channel + " " + self.user + " " + self.text


    def sent_at(self, id):
        """Does the message contain an at mention of the user identified by id."""
        return "<@" + id + ">" in self.text


    def is_direct(self):
        """Checks if the message is sent on a direct message channel"""
        return self.channel.startswith("D")



class Bot():
    """ Abstract Slack bot """

    def __init__(self, bot_name, bot_token):
        self.bot_id = None
        self.bot_name = bot_name
        self.bot_token = bot_token
        self.sleep_time = 1


    def connect(self):
        """Connect to Slack"""
        self.slack_client = SlackClient(self.bot_token)
        if self.slack_client.rtm_connect():
            print("Bot is running!")
            self.bot_id = self._get_id()
        else:
            raise Exception("Failed to connect. Check bot name and token.")


    def listen(self):
        """Start listening to events using the real time messaging API"""
        while True:
            rtm_events = self.slack_client.rtm_read()
            self.handle_events(rtm_events)
            time.sleep(self.sleep_time)


    def say(self, channel, text):
        """Say a message to a channel"""
        self.slack_client.api_call(
          "chat.postMessage", channel=channel,
          text=text, as_user=True)


    def handle_message(self, message):
        """Subclass to implement"""
        print(message)


    def handle_events(self, rtm_events):
        """Reads the event list and returns any messages"""
        messages = []
        if (rtm_events and len(rtm_events) > 0):
            for rtm_event in rtm_events:
                # Bot only cares about message events for now
                if "type" in rtm_event and rtm_event["type"] == "message":
                    msg = Message(rtm_event)
                    # Don't handle own messages
                    if (msg.user != self.bot_id):
                        self.handle_message(msg)


    def _get_id(self):
        """Finds the bot's ID using the API"""
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return user.get("id")
        else:
            raise Exception("Failed to resolve the bot ID")
