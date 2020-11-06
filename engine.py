import pandas
import string
import sys
import os
import pprint
import random

from functools import partial

sys.path.append('./io/')
from reader import read_yaml
sys.path.append('./resources/')
import openstack as os
import create_domain
import create_project
import create_network
import create_student
import create_machine


##### USER DEFINED CONSTANT #####
OS_PASSWORD = 'OS_PASSWORD'
OS_USERNAME = 'OS_USERNAME'
OS_PROJECT = 'OS_PROJECT_NAME'
OS_PROJECT_DOMAIN = 'OS_PROJECT_DOMAIN_NAME'
OS_AUTH_URL = 'OS_AUTH_URL'
OS_USER_DOMAIN = 'OS_USER_DOMAIN_NAME'
ADMIN = 'admin'
NAME = 'Name'
DOMAIN = 'Domain'
PROJECT = 'Project'
NETWORKS = 'Networks'
STUDENTS = 'Students'
MACHINES = 'Machines'
CIDR = 'CIDR'
PROVIDER = 'Provider'
USERNAME = 'Username'
PER_PROJECT = 'PerProject'
PER_STUDENT = 'PerStudent'

##### COMMAND LINE ARGUMENTS #####
CLASSROOM_FILE = sys.argv[1]

ledger = {}
def start():
  # Meat & Substance: This function is the "main" function of the file, it creates vm's for users from a csv file.
  [classroom, _] = read_yaml(CLASSROOM_FILE)
  ledger[DOMAIN] = create_domain.create_domain('default')
  ledger[PROJECT] = create_project.create_project(classroom[PROJECT][NAME], ADMIN, ADMIN)
  ledger[NETWORKS] = map(partial(create_network.create_linked_network, ledger[DOMAIN], ledger[PROJECT]), classroom[NETWORKS])
  ledger[STUDENTS] = map(partial(create_student.create_student, ledger), classroom[STUDENTS])
  ledger[MACHINES] = map(partial(create_machine.create_project_machines, ledger), classroom[MACHINES][PER_PROJECT]) + map(partial(create_machine.create_student_machines, ledger), classroom[MACHINES][PER_STUDENT])

if __name__ == '__main__': # Program entrance
    print ('Testing engine.py {}'.format(CLASSROOM_FILE))
    start()
