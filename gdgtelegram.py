#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from unidecode import unidecode
import json
import urllib2



# loading token from config file
tokenconf = open('token.conf', 'r').read()
tokenconf = tokenconf.replace("\n", "")
TOKEN = tokenconf

# Enable logging
logging.basicConfig(filename='gdgtgbot.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)





# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):

	
	bot.sendMessage(update.message.chat_id, text="Start")


def help(bot, update):
	bot.sendMessage(update.message.chat_id, text='Help!')

#/gdg-get ezine (last||num)
def ezine_handle(bot,update):
	
	try:

		msg=update.message.text
		msg=msg.split(' ')
		print msg

		#these url are only for testing

		last_url='http://www.unict.it/sites/default/files/guida_1617_small_cert.pdf'
		one_url='http://www.unict.it/sites/default/files/Guida%20autocertificazione%20reddituale.pdf'

		temp_file='ezine.pdf'

		url=''

		if msg[2]=='last':
			url=last_url
		else:
			url=one_url
	
		print 'downloading %s\n' % url
		response = urllib2.urlopen(url)

		with open(temp_file,'w') as f:
			f.write(response.read())
			f.close()
			print 'Downloaded'
	
		with open(temp_file,'r') as f:
			bot.sendDocument(chat_id=update.message.chat_id,document=f)
	
	except Exception as e:
		logger.exception('Update "%s" caused an error "%s"' % (update,e))


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():

	



	updater = Updater(TOKEN)

	dp = updater.dispatcher


	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))

	dp.add_handler(CommandHandler("gdg-get", ezine_handle))
	



	dp.add_error_handler(error)


	updater.start_polling()

	logger.info('Bot started!')
	print 'Bot Started\n'

	updater.idle()


if __name__ == '__main__':
	main()
