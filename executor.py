import pandas
import string
import random
import sys
import os
import pprint
from reader import read_yaml


##### USER DEFINED CONSTANT #####
OS_PASSWORD = 'OS_PASSWORD'
OS_USERNAME = 'OS_USERNAME'
OS_PROJECT = 'OS_PROJECT_NAME'
OS_PROJECT_DOMAIN = 'OS_PROJECT_DOMAIN_NAME'
OS_AUTH_URL = 'OS_AUTH_URL'
OS_USER_DOMAIN = 'OS_USER_DOMAIN_NAME'

##### COMMAND LINE ARGUMENTS #####
YAML_FILE = sys.argv[1]

##### USER DEFINED VARIABLE #####
student_dataframe = pd.read_csv(CSV_FILE_NAME)
rows = student_dataframe.T.to_dict().values()

def validate():
    if NETWORK_ID==None:
        return 'network id cannot be null'
    if IMAGE_ID==None:
        return 'image id cannot be null'
    if FLAVOR_ID==None:
        return 'flavor id cannot be null'
    if CSV_FILE_NAME==None:
        return 'CSV cannot be null'

def start():
