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
class ActionInstanceHandler:

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
            print("[YET TO IMPLEMENT] Remove action instance ")
        
        # cycle over NEW actions and create a REST resource
        for a in added:
            
            # retrieve action URI and name
            logging.debug(a)
            actionUri = a["action"]["value"]
            actionInstance = a["instance"]["value"]
            try:
                inputData = a["inputData"]["value"]
                inputValue = a["value"]["value"]
            except:
                inputData = None
                inputValue = None
                
            # check if the thing is in the dictionary, otherwise it is a problem
            if thingUri in self.thingsDict:

                # add the action instance to the dictionary            
                self.thingsDict[thingUri]["actions"][actionUri]["instances"] = {}

                # check if the instance was already detected
                if not actionInstance in  self.thingsDict[thingUri]["actions"][actionUri]["instances"]:
                    self.thingsDict[thingUri]["actions"][actionUri]["instances"][actionInstance] = {}
                    self.thingsDict[thingUri]["actions"][actionUri]["instances"][actionInstance]["input"] = {}
                    self.thingsDict[thingUri]["actions"][actionUri]["instances"][actionInstance]["id"] = str(uuid.uuid4()).split("-")[0]

                # store input data, if any
                if inputData:
                    self.thingsDict[thingUri]["actions"][actionUri]["instances"]["input"][inputData] = inputValue
            
            # create the rest resources
            uri = '/things/' + self.thingsDict[thingUri]["id"] + "/actions/" + self.thingsDict[thingUri]["actions"][actionUri]["id"] + "/instances/" + self.thingsDict[thingUri]["actions"][actionUri]["instances"][actionInstance]["id"]
            logging.debug("Adding route: " + self.baseURL + uri)
            self.flaskApp.add_url_rule(uri, actionUri, self.invFunct)

        # release the lock
        self.lock.release()
