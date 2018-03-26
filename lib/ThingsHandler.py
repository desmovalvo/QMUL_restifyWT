#!/usr/bin/python3

# global reqs
import logging
import threading
from uuid import uuid4
from flask import Flask
from flask import request
from sepy.JSAPObject import JSAPObject
from sepy.LowLevelKP import LowLevelKP
from sepy.BasicHandler import BasicHandler


# the handler
class ThingsHandler:

    # constructor
    def __init__(self, flaskApp, invokedFunction, things):

        # store parameters
        self.flaskApp = flaskApp
        self.invFunct = invokedFunction
        self.thingsDict = things
        self.baseURL = "http://localhost:5000"

        # initialize a lock
        self.lock = threading.Lock()
        

    # handle
    def handle(self, added, removed):

        # acquire a lock
        self.lock.acquire()
        
        # cycle over OLD things
        for r in removed:

            logging.debug("Parsing removed binding:")
            print(r)
            
            ### things

            # 1 - retrieve the thing name
            thing = r["thing"]["value"]
            tName = r["tName"]["value"]

            # 2 - TODO - remove REST routes
            if thing in self.thingsDict:
                logging.debug("Removing routes for id: " + self.thingsDict[thing]["id"])
            
        
        # cycle over NEW things and create a REST resource
        for a in added:

            logging.debug("Parsing added binding:")
            print(a)

            ### things

            # 1 - retrieve the thing name
            thing = a["thing"]["value"]
            tName = a["tName"]["value"]

            # 2 - add the thing to the dictionary and built default routes
            if not thing in self.thingsDict:

                # 2.0 - debug print
                logging.debug("Adding new thing " + thing)
                
                # 2.1 - bind an ID to the thing
                self.thingsDict[thing] = {}                
                self.thingsDict[thing]["id"] = str(uuid4()).split("-")[0]
            
                # 2.2 - add the default routes
                logging.debug("Adding basic REST resources for thing:")
                logging.debug(self.baseURL + '/' + self.thingsDict[thing]["id"])
                logging.debug(self.baseURL + '/' + self.thingsDict[thing]["id"] + "/events")
                logging.debug(self.baseURL + '/' + self.thingsDict[thing]["id"] + "/actions")
                logging.debug(self.baseURL + '/' + self.thingsDict[thing]["id"] + "/properties")
                self.flaskApp.add_url_rule('/' + self.thingsDict[thing]["id"], "td", self.invFunct)
                self.flaskApp.add_url_rule('/' + self.thingsDict[thing]["id"] + "/events", "events", self.invFunct)
                self.flaskApp.add_url_rule('/' + self.thingsDict[thing]["id"] + "/actions", "actions", self.invFunct)
                self.flaskApp.add_url_rule('/' + self.thingsDict[thing]["id"] + "/properties", "properties", self.invFunct)

            # 3 - fill the dictionary
            self.thingsDict[thing]["name"] = tName
            self.thingsDict[thing]["properties"] = {}
            self.thingsDict[thing]["actions"] = {}
            self.thingsDict[thing]["events"] = {}
        

        # release a lock
        self.lock.release()
