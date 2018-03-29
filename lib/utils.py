#!/usr/bin/python

import logging


def get_thing_description(thing_dict, thing_id, ape_id=None, ape_type=None):

    logging.getLogger('restifyWT')
    
    for t in thing_dict:
        if thing_dict[t]["id"] == thing_id:
            if not ape_id:
                return t, thing_dict[t]
            else:
                for a in thing_dict[t][ape_type]:
                    if thing_dict[t][ape_type][a]["id"] == ape_id:
                        return t, thing_dict[t], a

                    
def get_instance_details(thing_dict, thing_id, ape_id, ape_type, instance_id):

    logging.getLogger('restify')

    # initialize output structure
    outStruct = {}
    if ape_type == "events":
        outStruct["event"] = ape_id
    else:
        outStruct["action"] = ape_id        
    outStruct["thingID"] = thing_id

    # iterate over things
    for t in thing_dict:
        if thing_dict[t]["id"] == thing_id:

            # iterate over actions/events
            for a in thing_dict[t][ape_type]:
                if thing_dict[t][ape_type][a]["id"] == ape_id:

                    # iterate over instances
                    for i in thing_dict[t][ape_type][a]["instances"]:
                        if thing_dict[t][ape_type][a]["instances"][i]["id"] == instance_id:
                            outStruct["instance"] = thing_dict[t][ape_type][a]["instances"][i]

    # return
    return outStruct
                        
