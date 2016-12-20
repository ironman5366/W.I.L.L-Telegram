#Internal imports
from plugin_handler import subscribe
import logging

#External imports
import wolframalpha

log = logging.getLogger()

def search_wolfam():
    pass
    #TODO: use dataset to search the db for the wolfram api key

@subscribe({"sentence_type":"question"})
def main(query):
    '''Start the search'''
    log.info("In main search function with query {0}".format(query))