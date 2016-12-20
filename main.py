#Builtin modules
import logging
import os

#Internal modules
import interface

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#TODO: get wolframalpha stuff

class main():
    '''Start W.I.L.L and determine data status'''
    def __init__(self):
        '''Call starting functions'''
        #Bot token should be held in a file named token.txt
        if os.path.isfile("token.txt"):
            token = open('token.txt').read()
            log.info("Bot token is {0}".format(token))
            log.info("Starting the telegram interface")
            #Start the telegram bot
            interface.initialize(token)
        else:
            log.error(
                '''
                Couldn't find the file containing the api token.
                Please create a file named token.txt in /usr/local/W.I.L.L-Telegram containing the token.
                '''
            )
if __name__ == "__main__":
    log = logging.getLogger()
    log.info("Starting W.I.L.L")
    main()