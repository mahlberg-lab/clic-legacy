# This file contains the project wide settings. It is not
# part of version control and it should be adapted to
# suit each deployment. 

from os import environ


# Use the absolute path to the directory that stores the data.
# This can differ per deployment
DATA_DIRECTORY = "/cheshire3/clic/dbs/dickens/data/"

#TODO: make the cache settings imported in api.py
CACHE_DIR = ""
CACHE_LOCK = ""

# Check whether there are local settings.
# If there are, then overwrite the above settings
# with the specific settings defined in the local settings

try: 
    environ['CLIC_SETTINGS'] == 'local'
    from local_settings import *
    print 'Using the local settings (local_settings.py)'

except KeyError:
    print 'Using the standard settings file (settings.py)'

