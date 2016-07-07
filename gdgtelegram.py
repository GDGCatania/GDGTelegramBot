#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from unidecode import unidecode
import json




# loading token from config file
tokenconf = open('token.conf', 'r').read()
tokenconf = tokenconf.replace("\n", "")
TOKEN = tokenconf

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)





# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):

	
	bot.sendMessage(update.message.chat_id, text="Start")


def help(bot, update):
	bot.sendMessage(update.message.chat_id, text='Help!')


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():

	



	updater = Updater(TOKEN)

	dp = updater.dispatcher


	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	



	dp.add_error_handler(error)


	updater.start_polling()

	logger.info('Bot started!')

	updater.idle()


if __name__ == '__main__':
	main()
