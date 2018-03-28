#!/usr/bin/python

import logging


def get_thing_description(thing_dict, thing_id, ape_id=None, ape_type=None):

    logging.getLogger('restifyWT')
    
    for t in thing_dict:
        if thing_dict[t]["id"] == thing_id:
            if not ape_id:
                return t, thing_dict[t]
            else:
                if ape_type == "actions":
                    for a in thing_dict[t]["actions"]:
                        if thing_dict[t]["actions"][a]["id"] == ape_id:
                            return t, thing_dict[t], a
                elif ape_type == "properties":
                    for a in thing_dict[t]["properties"]:
                        if thing_dict[t]["properties"][a]["id"] == ape_id:
                            return t, thing_dict[t], a
