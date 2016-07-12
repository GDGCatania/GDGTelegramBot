# GDGTelegramBot
Telegram Bot for the GDGCatania group

## How it works?

Uses standard (python-telegram-bot library)[https://github.com/python-telegram-bot/python-telegram-bot]

## Running the Bot Locally

The first step to run the bot is to install the required dependencies. You can do this via **pip**

```
$ pip install python-telegram-bot --upgrade
$ pip install unidecode
```

Then call the @BotFather within telegram and use the `/newbot` to create a new bot. Then do the following:

```
$ touch token.conf

# Open token.conf using your favourite editor
# Paste the bot's token in the first line of the configuration file
# Add an empty line at the end of the file
```

Then run:

```
$ python gdgtelegram.py
```

## Testing the deployed Bot

You can test it by add [GDGTelegramBot](http://telegram.me/GDGTelegramBot) to your Telegram


## License

This open-source software is published under the GNU General Public License (GNU GPL) version 3. Please refer to the "LICENSE" file of this project for the full text.
