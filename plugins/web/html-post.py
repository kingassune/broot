import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
from printlib import *
import requires

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from var import global_vars



###########################
#SECTION 2 - ABOUT
###########################
name = "html-post"
description = '''
This plugin is used to bruteforce a simple HTTP POST request.  You'll
need the html for the username and password fields.

Extra Help: Use only the Target Fields for your url
Example: set target http://10.0.0.1:8443
'''
author = "midnightseer"
version = "1.0"
art = """


"""
banner = '''
{}
{}
Author:  {}
Version: {}'''.format(art,name,author,version)
print(banner)

#############################
#SECTION 3 - PLUGIN COMMANDS
#############################

#This is an example, you do not necessarily need extra commands.  Replace the below with your own
plugin_cmds = {
    # "test": {
    #         "Command": "test",
    #         "Help": "Print information related to the subsequent key-word.",
    #         "Sub-Cmds": ["commands", "plugins", "options", "loaded-plugin", "creds", "sequence"],
    #         "Usage": "test <sub-cmd>",
    #         "Alias": None
    #     },
}

#function to define what to do with the new commands
def parse_plugin_cmds(commands):
    cmds = commands.split(" ")
    if cmds[0] == "test":
        print("success!")
    pass

#############################
#SECTION 4 - PLUGIN VARIABLES
#############################

#This is an example, variables must have a unique name
plugin_vars = {
    'POST-Password': {
        "Name": "Password",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "This value is the password id value from the html form.",
        "Example": "|<input id=password-id>| {password-id} is the value."
    },
    'POST-Username': {
        "Name": "Username",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "This value is the password id value from the html form.",
        "Example": "|<input id=username-id>| {password-id} is the value." 
    }
}

#############################
#SECTION 5 - VALIDATE
#############################
#This function is used to validate your plugin variables prior to execution.  
#'Broot" calles this function immediately after 'run' and upon 'validate.'
#This function does not need to be filled out but the skeleton structure here
#is required. 

def validate():
    validated = True        # Technically, field values can have numbers, letters, and special chars, no validation needed
    score = 0
    if plugin_vars['POST-Password']['Value'] is None:
        validated = False
        print_fail("POST-Password is a required field")
    if plugin_vars['POST-Username']['Value'] is None:
        validated = False
        print_fail("POST-Username is a required field")
    if "<" in plugin_vars['POST-Password']['Value'] or ">" in plugin_vars['POST-Password']['Value']:
        validated = False
        print_fail("POST-Password should not contain html brackets")
    if "<" in plugin_vars['POST-Username']['Value'] or ">" in plugin_vars['POST-Username']['Value']:
        validated = False
        print_fail("POST-Username should not contain html brackets")
    return validated

#############################
#SECTION 6 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE

#Default Port - if you have a default port to auto fill some variable, enter it here.
#global_vars['target-port']['Value'] = 80

def run(username, password, target, port):
    attempt = "Target:{}:{} Username:{} Password:{}".format(target, port, username, password) # for printing messages if you want to
    verbose = global_vars['verbose']['Value']
    post_payload = {
        plugin_vars['POST-Username']['Name']: plugin_vars['POST-Username']['Value'],
        plugin_vars['POST-Password']['Name']: plugin_vars['POST-Password']['Value']
    }
    try:
        html = requests.post(target, data = post_payload)
        print(html.text)
    except Exception as e:
        if verbose:
            print_fail(e)
    print
    #return True or False  -- must return True if the authentication attempt was successful and false if it failed
