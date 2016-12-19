#Builtin imports
import logging
#External imports
from telegram.ext import Updater, CommandHandler
#Internal imports

log = logging.getLogger()

events = {}

help_str = "TODO: write help_str"

def help(bot, update):
    update.message.reply_text(help_str)


def start(bot,update):
    '''First run commands'''
    #TODO: add database creation here
    update.message.reply_text("Welcome to W.I.L.L!\n What's your name?")
    #TODO: add conversation handlers
def error(bot, update, error):
    log.warn('Update "%s" caused error "%s"' % (update, error))

def parse(bot, update):
    pass
def initialize(bot_token):
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, parse))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()