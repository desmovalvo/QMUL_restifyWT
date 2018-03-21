#!/usr/bin/python3

# global reqs
import logging
from flask import Flask
from flask import request
from sepy.JSAPObject import JSAPObject
from sepy.LowLevelKP import LowLevelKP
from sepy.BasicHandler import BasicHandler

# the handler
class ActionHandler:

    # constructor
    def __init__(self, flaskApp, invokedFunction):

        # store parameters
        self.flaskApp = flaskApp
        self.invFunct = invokedFunction    
        
    # handle
    def handle(self, added, removed):

        # cycle over NEW actions and create a REST resource
        for a in added:

            # retrieve action URI and name
            actionUri = a["action"]["value"]
            actionName = a["actionName"]["value"]

            # create the rest resource
            self.flaskApp.add_url_rule('/' + actionName, actionName, self.invFunct)
            logging.debug("Creating a the resource /" + actionName)
    

        # cycle over OLD actions and delete their REST resources

