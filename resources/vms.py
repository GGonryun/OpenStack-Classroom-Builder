from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as k_client
from novaclient import client as n_client
import pandas as pd
import string
import random
import sys
import os
from hashlib import pbkdf2_hmac
import binascii
import pprint

# INSTRUCTIONS:
# This script should be run before a user has logged on to change their password.
# This script assumes you have loaded in the required variables to log into the CLI.
# This script assumes the csv file is located in the same directory.
# The CSV file must have non-nullable columns: Username, Project.
# The CSV file may have nullable columns: Password (If included, the specified password is used instead).

# use: python create_vms image_id metasploitable flavor_id network_id users.csv
#      derive value for flavor_id from: openstack flavor list
#      derive value for network_id from: openstack network list
#      derive value for image_id from: openstack image list

##### USER DEFINED CONSTANT #####
OS_PASSWORD = 'OS_PASSWORD'
OS_USERNAME = 'OS_USERNAME'
OS_PROJECT = 'OS_PROJECT_NAME'
OS_PROJECT_DOMAIN = 'OS_PROJECT_DOMAIN_NAME'
OS_AUTH_URL = 'OS_AUTH_URL'
OS_USER_DOMAIN = 'OS_USER_DOMAIN_NAME'

##### COMMAND LINE ARGUMENTS #####
IMAGE_ID = sys.argv[1]
IMAGE_NAME = sys.argv[2]
FLAVOR_ID = sys.argv[3]
NETWORK_ID = sys.argv[4]
CSV_FILE_NAME = sys.argv[5]

def validate_input():
    if NETWORK_ID==None:
        return 'network id cannot be null'
    if IMAGE_ID==None:
        return 'image id cannot be null'
    if FLAVOR_ID==None:
        return 'flavor id cannot be null'
    if CSV_FILE_NAME==None:
        return 'CSV cannot be null'

##### USER DEFINED VARIABLE #####
student_dataframe = pd.read_csv(CSV_FILE_NAME)
rows = student_dataframe.T.to_dict().values()

# Copied from create_users.py
def generate_hash(salt, password):
    derived_key = pbkdf2_hmac('sha512', password, salt, 500)
    new_password = binascii.hexlify(derived_key)[0:9]
    return new_password

# create each students password
for row in rows:
    if not 'Password' in row:
        # we try to recreate the original hash from the username and the original salt.
        row['Password'] = generate_hash('plsnohack', row['Username'])

# utility function to access environment variables.
def env(name):
    if name in os.environ:
        return os.environ[name]
    else:
        raise Exception('{} does not exist as an environment variable!'.format(name))

# utility function that creates an authenticated keystone client, uses environment variables.
def create_keystone_client():
    auth = v3.Password(auth_url=env(OS_AUTH_URL),
                       username=env(OS_USERNAME),
                       password=env(OS_PASSWORD),
                       project_name=env(OS_PROJECT),
                       user_domain_name=env(OS_USER_DOMAIN),
                       project_domain_name=env(OS_PROJECT_DOMAIN))

    sess = session.Session(auth=auth)
    keystone = k_client.Client(session=sess)
    return keystone

# Nova clients are created to be project specific, the project id identifies which nova client to use.
# If a nova client does not exist, a process-long client must be opened and stored in this list.
nova_clients = {}
def create_nova_client(project, username, password):
    if not project in nova_clients:
        auth = v3.Password(auth_url=env(OS_AUTH_URL),
                       username=username,
                       password=password,
                       project_name=project,
                       user_domain_name=env(OS_USER_DOMAIN),
                       project_domain_name=env(OS_PROJECT_DOMAIN))

        sess = session.Session(auth=auth)
        pprint.pprint('create session success: username {}, project {}'.format(username, project))
        nova_clients[project] = n_client.Client(2, session=sess)
    return nova_clients[project]


# Meat & Substance: This function is the "main" function of the file, it creates vm's for users from a csv file.
def create_vms():
    keystone = create_keystone_client();
    created_vms = []
    for row in rows:
        vm = create_vm(row);
        created_vms.append(vm)
    pprint.pprint(created_vms)

def create_vm(row):
    username = row['Username']
    vm_name = username + '-' + IMAGE_NAME
    try:
        vm_name = username + '-' + IMAGE_NAME
        nova_client = create_nova_client(row['Project'], username, row['Password'])
        nic_d = [{ 'net-id': NETWORK_ID }]
        pprint.pprint("create vm success: vm {}, user {}, flavor: {}".format(vm_name, username, FLAVOR_ID))
        return nova_client.servers.create(name=vm_name, image=IMAGE_ID, flavor=FLAVOR_ID, nics=nic_d)
    except:
        pprint.pprint("an error has occured creating {}, {}, {}, {}, {}".format(username, vm_name, IMAGE_ID, FLAVOR_ID, NETWORK_ID))
        return None

error = validate_input();
if error==None:
    create_vms();
else:
    pprint.pprint("invalid cli input {}".format(error))
