#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from unidecode import unidecode
import json
import urllib2

# Enable logging
logging.basicConfig(filename='gdgtgbot.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)

# loading token from config file
logger.info('Loading token from file...')
tokenconf = open('token.conf', 'r').read()
tokenconf = tokenconf.replace("\n", "")
TOKEN = tokenconf

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start_handle(bot, update):
	bot.sendMessage(update.message.chat_id, text=
		"Hello and Welcome to the GDGCatania's Bot!\n" \
		"Type /help for more")

def help_handle(bot, update):
	help = 'Hello! This is the GDG Bot :) \n'\
			'Use the following comments for help: \n'\
			'/ezine [last or number]'
	bot.sendMessage(update.message.chat_id, text=help)

#/gdg-get ezine (last||num)
def ezine_handle(bot,update):
	logger.info('Serving: %s message: %s\n' % (update.message.from_user.id, update.message.text))
	
	base_url='http://gdgcatania.org/gdg-get.php?res=ezine-'
	try:
		msg=update.message.text.split(' ')	

		if len(msg) != 2:
			bot.sendMessage(update.message.chat_id, text="Please provide only one parameter for this command")
			return

		url = base_url + msg[1]
	
		logger.info('Connecting to %s\n' % url)

		response = urllib2.urlopen(url)
		resource_url=response.read()

		logger.info('Response is %s\n' % resource_url)

		if  not 'ERROR:' in resource_url:
			temp_file='/tmp/%s_%s.pdf'% (resource_url.split('/')[-1].split('.')[0],update.message.from_user.id)
		
			logger.info('Temp file is %s\n' % temp_file)
			logger.info('Downloading %s\n' % resource_url)			

			response = urllib2.urlopen(resource_url)

			with open(temp_file,'w') as f:
				f.write(response.read())
				f.close()
				logger.info('Downloaded %s\n' % temp_file)
	
			with open(temp_file,'r') as f:
				logger.info('Sending to user %s\n' % update.message.from_user.id)
				bot.sendDocument(chat_id=update.message.chat_id, document=f)
				logger.info('%s sendend to %s\n' % (temp_file, update.message.from_user.id))
		else:
			bot.sendMessage(update.message.chat_id, text=resource_url.split(':')[-1])
			logger.info('File not found!')	
		
	except Exception as e:
		logger.exception('Update "%s" caused an error "%s"' % (update,e))


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


START_CMD = "start"
HELP_CMD = "help"
EZINE_CMD = "ezine"

def main():
	logger.info('Starting Bot!')
	updater = Updater(TOKEN)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler(START_CMD, start_handle))
	dp.add_handler(CommandHandler(HELP_CMD, help_handle))
	dp.add_handler(CommandHandler(EZINE_CMD, ezine_handle))
	
	dp.add_error_handler(error)

	updater.start_polling()
	logger.info('Bot started!')

	updater.idle()

if __name__ == '__main__':
	main()
