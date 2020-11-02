import pandas
import string
import random
import sys
import os
import pprint
sys.path.append('./io/')
from reader import read_yaml
sys.path.append('./resources/')
import openstack as os

##### USER DEFINED CONSTANT #####
OS_PASSWORD = 'OS_PASSWORD'
OS_USERNAME = 'OS_USERNAME'
OS_PROJECT = 'OS_PROJECT_NAME'
OS_PROJECT_DOMAIN = 'OS_PROJECT_DOMAIN_NAME'
OS_AUTH_URL = 'OS_AUTH_URL'
OS_USER_DOMAIN = 'OS_USER_DOMAIN_NAME'
DOMAIN = 'Domain'
PROJECT = 'Project'
NETWORKS = 'Networks'
STUDENTS = 'Students'
MACHINES = 'Machines'

##### COMMAND LINE ARGUMENTS #####
CLASSROOM_FILE = sys.argv[1]

ledger = {}
def start():
  # Meat & Substance: This function is the "main" function of the file, it creates vm's for users from a csv file.
  classroom = read_yaml(CLASSROOM_FILE)
  ledger[DOMAIN] = client.get_domain(classroom[DOMAIN])
  ledger[PROJECT] = client.get_project(classroom[PROJECT])
  
  # if(classroom[NETWORKS] != None):
  #   ledger[NETWORKS] = client.get_networks()
  # if(classroom[STUDENTS] != None):
  #   ledger[STUDENTS] = client.get_students()
  # if(classroom[MACHINES] != None):
  #   ledger[MACHINES] = client.get_machines()
def create_vms(classroom):
  userMachines = machines[PER_USER_KEY]
  projectMachines = machines[PER_PROJECT_KEY]



if __name__ == '__main__': # Program entrance
    print ('Testing engine.py {}'.format(CLASSROOM_FILE))
    start()
