# cowsay-slackbot

    ______________________________________
    | I'm mansikki, please treat me gently |
    --------------------------------------
     \   ^__^
      \  (oo)\_______
         (__)\       )\/\
             ||----w |
             ||     ||


Your friendly neighbourhood slackbot using cowsay, wrapping few things together:

- Cool ASCII graphics to enliven your slack with custom messages
- Fortune output for the cowsay animals
- Output a route suggestion in the Helsinki region, based on routahe
- Gofore Seppo makes an ASCII cameo

## Requirements for running the thing / development:
- Python (2.7)
- Virtuanenv installation

    - run "virtualenv mansikkibot"

    - run "source mansikkibot/bin/activate" to separate environment from the rest of your environment

- For using the routing command you need routahe (+ node and npm)

    - install node locally

    - install npm locally

    - install routahe by installing dependencies defined in package.json "npm install"

- Environment variables required for running:

  - BOT_NAME - Username of the bot (like: mansikkibot)
  - SLACK_BOT_TOKEN - Bot token

- Optionals:
  - COWPATH - You may change the path variable and include the seppo cowfile included in this repository

For your convenience the project supports .env file for providing the environment variable to your application during the initialization.

## Usage in Slack

Bot responds with the text that was in the message when it is mentioned or a direct message is sent to it.

Usage:

[!cowsay] [!fortune] [!cowfile "cowfile name"] [!routahe "From Address" "To Address"] [text [text ...]]

- `!cowsay` - At the moment, a compulsory command to output anything with mansikki. Needs to be chained with other commands.
- `!fortune` - Outputs a fortune. Can be combined with !cowfile but no other text.
- `!cowfile <cowfile>` - Uses a specific cowfile.
- `!routahe "<from>" "<to>"` - Use routahe routing (from, to) and output to chat
- Text - Freeform textual content output

Only one output type can be put out at a time. Preference order: fortune, routahe, text

TODO:
- Make the bot say things on a channel based on instructions given to it in a direct message.
- Something something in the month of May

## Screenshot
![Mansikki in action](https://vrpl.github.io/images/mansikkibot-screenshot.png)
