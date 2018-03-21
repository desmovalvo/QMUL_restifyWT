#!/usr/bin/python

# global reqs
import logging
from flask import Flask
from flask import request
from random import randint
from sepy.JSAPObject import JSAPObject
from sepy.LowLevelKP import LowLevelKP

# local reqs
from lib.ActionHandler import ActionHandler

# constants
CONFIG_FILE = "restifyWT.jsap"

# vars
jsap = None
kp = None

# flask app
app = Flask(__name__)

# my function
def myFunc():

    # debug
    logging.debug("New request through REST APIs.")
    print(request)
    logging.debug("Resource: %s -- Method: %s" % ("A", request.method))
    return "Done!"


# main
if __name__ == "__main__":

    # configure logging
    logger = logging.getLogger('restifyWT')
    logging.basicConfig(format='[%(levelname)s][%(funcName)s] %(message)s', level=logging.DEBUG)
    logging.debug("Logging subsystem initialized")
    
    # read the configuration file
    logging.debug("Loading JSAP config file")
    jsap = JSAPObject(CONFIG_FILE, 40)

    # connect to SEPA and subscribe to all the actions
    logging.debug("Initialize a KP")
    kp = LowLevelKP(None, 40)
    kp.subscribe(jsap.subscribeUri, jsap.getQuery("ACTIONS", {}), "actions", ActionHandler(app, myFunc))
    
    # start the main server
    logging.debug("Listening for requests...")
    app.run()
