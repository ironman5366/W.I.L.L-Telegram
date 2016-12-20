#Builtin imports
import logging
#External imports
import nltk
#Internal imports
import API

log = logging.getLogger()

def parse(command):
    '''Main sentence parsing class, using nltk'''
    log.info("Parsing command {0}".format(command))
    #Feed command into nltk
    tokens = nltk.word_tokenize(command)
    #Check for common lexical patterns
    #TODO: write a plugin parser