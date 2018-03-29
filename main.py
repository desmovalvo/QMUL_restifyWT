#!/usr/bin/python

# global reqs
import logging
from flask import Flask
from flask import request, render_template
from random import randint
from sepy.JSAPObject import JSAPObject
from sepy.LowLevelKP import LowLevelKP

# local reqs
from lib.utils import *
from lib.ThingsHandler import ThingsHandler
from lib.ActionHandler import ActionHandler
from lib.PropertyHandler import PropertyHandler
from lib.ActionInstanceHandler import ActionInstanceHandler

# constants
CONFIG_FILE = "restifyWT.jsap"

# vars
things = {}
jsap = None
kp = None

# flask app
app = Flask(__name__)


# route finder
def routeFinder():

    # debug
    logging.debug("New request through REST APIs.")
    logging.debug("Resource: %s -- Method: %s" % (request.url, request.method))

    # determine what to do
    req_path = request.path
    
    # paths may be:
    # /things
    # /things/<ID_T>
    # /things/<ID_T>/properties
    # /things/<ID_T>/properties/<ID_P>
    # /things/<ID_T>/actions
    # /things/<ID_T>/actions/<ID_P>
    # /things/<ID_T>/actions/<ID_P>/instances
    # /things/<ID_T>/actions/<ID_P>/instances/<ID_I>
    # /things/<ID_T>/events
    # /things/<ID_T>/events/<ID_P>

    # explode the path
    path_elements = req_path.split("/")
    del path_elements[0]

    # first level of check
    if len(path_elements) == 1:

        # /things
        logging.info("Managing access to /things")

        # render
        return render_template("things.html", things=things)

    elif len(path_elements) == 2:

        # /things/<ID_T>
        logging.info("Managing access to /things/<ID_T>")

        # get thing ID
        thing_ID = path_elements[1]

        # render
        thingURI, thingDict = get_thing_description(things, thing_ID)
        return render_template("thingDescription.html", thing=thingDict, thingURI=thingURI)
        
    elif len(path_elements) == 3:

        # get thing ID and second element of path
        thing_ID = path_elements[1]
        ape = path_elements[2] 
        
        # /things/<ID_T>/properties
        # /things/<ID_T>/events
        # /things/<ID_T>/actions

        # render
        thingURI, thingDict = get_thing_description(things, thing_ID)
        if ape == "actions":
            return render_template("actions.html", thing=thingDict, thingURI=thingURI)
        elif ape == "properties":
            return render_template("properties.html", thing=thingDict, thingURI=thingURI)
        elif ape == "events":
            return render_template("events.html", thing=thingDict, thingURI=thingURI)        
    
    elif len(path_elements) == 4:

        # get thing ID, second element of path and second id
        thing_ID = path_elements[1]
        ape = path_elements[2]
        ape_id = path_elements[3]
                
        # /things/<ID_T>/properties/<ID_P>
        # /things/<ID_T>/actions/<ID_P>
        # /things/<ID_T>/events/<ID_P>

        # render
        thingURI, thingDict, apeURI = get_thing_description(things, thing_ID, ape_id, ape)
        if ape == "actions":
            return render_template("action.html", thing=thingDict, thingURI=thingURI, thingID=thing_ID, actionID=ape_id, actionURI=apeURI)
        elif ape == "properties":
            return render_template("property.html", thing=thingDict, thingURI=thingURI, thingID=thing_ID, propID=ape_id, propURI=apeURI)
        elif ape == "events":
            return render_template("event.html", thing=thingDict, thingURI=thingURI, thingID=thing_ID, propID=ape_id, propURI=apeURI)

    elif len(path_elements) == 5:

        # get thing ID, second element of path and second id
        thing_ID = path_elements[1]
        ae = path_elements[2]
        ae_id = path_elements[3]
        
        # render
        thingURI, thingDict, aeURI = get_thing_description(things, thing_ID, ae_id, ae)
        if ae == "actions":
            return render_template("action_instances.html", thing=thingDict, thingURI=thingURI, thingID=thing_ID, actionID=ae_id, actionURI=aeURI)
#        elif ape == "events":
#            return render_template("event_instance.html", thing=thingDict, thingURI=thingURI, thingID=thing_ID, propID=ape_id, propURI=apeURI)

    elif len(path_elements) == 6:

        # get thing ID, second element of path and second id
        thing_ID = path_elements[1]
        ae = path_elements[2]
        ae_id = path_elements[3]
        i_id = path_elements[5]
        
        # render
        thingURI, thingDict, apeURI = get_instance_details(things, thing_ID, ape_id, ape, i_id)
        if ape == "actions":
            return render_template("action_instance.html", thing=thingDict, thingURI=thingURI, thingID=thing_ID, actionID=ape_id, actionURI=apeURI)
#        elif ape == "events":
#            return render_template("event_instance.html", thing=thingDict, thingURI=thingURI, thingID=thing_ID, propID=ape_id, propURI=apeURI)


        

# main
if __name__ == "__main__":

    # configure logging
    logger = logging.getLogger('restifyWT')
    logging.basicConfig(format='[%(levelname)s][%(funcName)s] %(message)s', level=logging.DEBUG)
    logging.debug("Logging subsystem initialized")
    
    # read the configuration file
    logging.debug("Loading JSAP config file")
    jsap = JSAPObject(CONFIG_FILE, 40)

    # add the basic resource /things
    logging.debug('http://localhost:5000/things')
    app.add_url_rule('/things', "things", routeFinder)
    
    # connect to SEPA and subscribe to all the actions
    logging.debug("Initialize a KP")
    kp = LowLevelKP(None, 40)
    kp.subscribe(jsap.subscribeUri, jsap.getQuery("THINGS", {}), "things", ThingsHandler(app, routeFinder, things))
    kp.subscribe(jsap.subscribeUri, jsap.getQuery("ACTIONS", {}), "actions", ActionHandler(app, routeFinder, things))
    kp.subscribe(jsap.subscribeUri, jsap.getQuery("PROPERTIES", {}), "properties", PropertyHandler(app, routeFinder, things))
    kp.subscribe(jsap.subscribeUri, jsap.getQuery("ACTION_INSTANCES", {}), "instances", ActionInstanceHandler(app, routeFinder, things))
    
    # start the main server
    logging.debug("Listening for requests...")
    app.run()
