from keystoneauth1.identity import v3
from keystoneauth1 import session
import sys
import os
from hashlib import pbkdf2_hmac
import binascii
import argparse
from keystoneclient.v3 import client as k_client
import pprint
import users_utility

## Description ##
## Create a user with the admin role and add them to the admin project. ##

# How to run ##
# python create_admin.py --create-admin <username> 
# python create_admin.py --show-password <username>
# note: the argument comes right after the flag command.

def create_admin_user(username):
    created_admin = {}
    # check if admin user already exists
    admin_exists = users_utility.get_user(username)
    if admin_exists:
        print('A user with the username ' + username + ' already exists.')
    else:
        # create an authenticated keystone client
        keystone = users_utility.create_keystone_client()
        user_password = users_utility.generate_user_password(username)
        admin_project_name = 'admin'
        admin_project_id = users_utility.get_a_projectID(admin_project_name)
        print('...Creating Admin User...')
        user = users_utility.create_single_user(username, user_password, admin_project_id, users_utility.ADMIN_ROLE)
        if user:
            created_admin['username'] = username
            created_admin['password'] = user_password
            pprint.pprint(created_admin)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-admin", help="The username of choice used to create an admin user.")
    parser.add_argument("--show-password", help="prints the successfully created admin user's credentials")
    args = parser.parse_args()

    if args.create_admin:
        create_admin_user(args.create_admin)
    elif args.show_password:
        # todo: Add a check if the user exists before showing the password
        password = users_utility.generate_user_password(args.show_password)
        pprint.pprint('The user ' + args.show_password + ' password: ' + password)
    else:
        raise Exception('create_admin.py usage: --create-admin <username> or --show-password <username>')

