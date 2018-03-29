#!/usr/bin/python3

# global reqs
import uuid
import logging
import threading
from flask import Flask
from flask import request
from sepy.JSAPObject import JSAPObject
from sepy.LowLevelKP import LowLevelKP
from sepy.BasicHandler import BasicHandler

# the handler
class ActionHandler:

    # constructor
    def __init__(self, flaskApp, invokedFunction, things):

        # store parameters
        self.flaskApp = flaskApp
        self.invFunct = invokedFunction
        self.thingsDict = things
        self.baseURL = "http://localhost:5000"
        self.lock = threading.Lock()
        
    # handle
    def handle(self, added, removed):

        # grab the lock
        self.lock.acquire()
        
        # cycle over OLD actions and delete their REST resources
        for r in removed:
            print("[YET TO IMPLEMENT] Remove action " + r["action"]["value"])
        
        # cycle over NEW actions and create a REST resource
        for a in added:
            
            # retrieve action URI and name
            thingUri = a["thing"]["value"]
            thingName = a["thingName"]["value"]
            actionUri = a["action"]["value"]
            actionName = a["actionName"]["value"]
            
            # check if the thing is already in the dictionary
            if not thingUri in self.thingsDict:
                self.thingsDict[thingUri] = {}
                self.thingsDict[thingUri]["events"] = {}
                self.thingsDict[thingUri]["actions"] = {}
                self.thingsDict[thingUri]["properties"] = {}
                self.thingsDict[thingUri]["id"] = str(uuid.uuid4()).split("-")[0]

            # add the action to the dictionary            
            self.thingsDict[thingUri]["actions"][actionUri] = {}
            self.thingsDict[thingUri]["actions"][actionUri]["name"] = actionName
            self.thingsDict[thingUri]["actions"][actionUri]["id"] = str(uuid.uuid4()).split("-")[0]
            
            # create the rest resources
            uri = '/things/' + self.thingsDict[thingUri]["id"] + "/actions/" + self.thingsDict[thingUri]["actions"][actionUri]["id"]
            logging.debug("Adding route: " + self.baseURL + uri)
            self.flaskApp.add_url_rule(uri, actionUri, self.invFunct)
            uri = '/things/' + self.thingsDict[thingUri]["id"] + "/actions/" + self.thingsDict[thingUri]["actions"][actionUri]["id"] + "/instances"
            logging.debug("Adding route: " + self.baseURL + uri)
            self.flaskApp.add_url_rule(uri, actionUri, self.invFunct)

        # release the lock
        self.lock.release()
