#!/usr/bin/python

import logging

def get_thing_description(thing_dict, thing_id):

    for t in thing_dict:
        if thing_dict[t]["id"] == thing_id:
            return t, thing_dict[t]
        

def get_action_description(thing_dict, thing_id, action_id):

    for t in thing_dict:
        if thing_dict[t]["id"] == thing_id:
            for a in thing_dict[t]["actions"]:
                if thing_dict[t]["actions"][a]["id"] == action_id:
                    return t, thing_dict[t], a
        
