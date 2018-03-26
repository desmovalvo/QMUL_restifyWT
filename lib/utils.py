#!/usr/bin/python

def get_thing_description(thing_dict, thing_id):

    for t in thing_dict:
        if thing_dict[t]["id"] == thing_id:
            return t, thing_dict[t]
        

def get_thing_events(thing_dict, thing_id):
    return thing_dict[thing_id]["events"]

def get_thing_actions(thing_dict, thing_id):
    return thing_dict[thing_id]["actions"]

def get_thing_properties(thing_dict, thing_id):
    return thing_dict[thing_id]["properties"]

