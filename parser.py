#Builtin imports
import logging
#External imports
import nltk
import zope.event
log = logging.getLogger()

def parse(command):
    '''Main sentence parsing class, using nltk'''
    log.info("Parsing command {0}".format(command))
    #Feed command into nltk
    tokens = nltk.word_tokenize(command)
    #Check for common lexical patterns
    tagged = nltk.pos_tag(tokens)
    #Start out by looking for recognized nouns
    verbs = []
    for i in tagged:
        if i[1] == "VB":
            verbs.append(i[0])
    log.info("Found verbs {0}".format(verbs))
    #TODO: write a plugin parser
    #TODO: have the plugins put in their own event hooks on initialize