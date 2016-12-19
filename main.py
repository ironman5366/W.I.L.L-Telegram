#Builtin modules
import logging
import os
import json
import sys

#Internal modules
import interface
import telegram

#TODO: switch to a permanent sqlalchemy db

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
class main():
    '''Start W.I.L.L and determine data status'''
    def __init__(self):
        '''Call starting functions'''
        #Check if the database is up
        #TODO: change to sqlalchemy code
        if os.path.isfile("will.json"):
            f = json.load("will.json")
            bot_token = f["bot_token"]
            interface.initialize(bot_token)
        else:
            log.error("Cannot find data store")
            sys.exit()




if __name__ == "__main__":
    log = logging.getLogger()
    log.info("Starting W.I.L.L")
    main()