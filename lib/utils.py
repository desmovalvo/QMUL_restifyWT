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
