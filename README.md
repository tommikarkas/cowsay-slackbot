# cowsay-gofore-slackbot

Requirements for development:

- install virtuanenv
-> run "virtualenv mansikkibot"
-> run "source mansikkibot/bin/activate" to separate environment from the rest of your environment


Environment variables required for running:

- BOT_NAME - Username of the bot (like: mansikkibot)
- SLACK_BOT_TOKEN - Bot token

Moo
 ______________________________________
< I'm mansikki, please treat me gently >
 --------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

## Usage in Slack

Bot responds with the text that was in the message when it is mentioned or a direct message is sent to it.

Commands:
- `!fortune` - Says a fortune. Can be combined with !cowfile but no other text.
- `!cowfile:<cowfile>` - Uses a specific cowfile.

TODO: 
- Make the bot say things on a channel based on instructions given to it in a direct message.
- Something something something

## Screenshot
![Mansikki in action](https://vrpl.github.io/images/mansikkibot-screenshot.png)
