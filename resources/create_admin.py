from keystoneauth1.identity import v3
from keystoneauth1 import session
from hashlib import pbkdf2_hmac
import binascii
from keystoneclient.v3 import client as k_client
import argparse
import sys
import os
import pprint
import users_utility

## Description ##
## Create a user with the admin role and add them to the admin project. ##

# How to run ##
# python create_admin.py --create-admin <username> 
# python create_admin.py --show-password <username>
# note: the argument comes right after the flag command.

def create_admin_user(username):
    print('create_admin_user(username): {}'.format(username))
    # check if admin user already exists
    admin_exists = users_utility.get_user(username)
    print('create_admin_user() => admin_exists: {}'.format(admin_exists))
    if admin_exists:
        print('create_admin_user() => An admin user with the username ' + username + ' already exists.')
    else:
        # create an authenticated keystone client
        keystone = users_utility.create_keystone_client()
        user_password = users_utility.generate_user_password(username)
        admin_project_name = 'admin'
        admin_project_id = users_utility.get_a_projectID(admin_project_name)
        user = users_utility.create_single_user(username, user_password, admin_project_id, users_utility.ADMIN_ROLE)
        print('create_admin_user() => does user exist? {}'.format(user))
        if user:
            print('create_admin_user() => succesfully created admin => username, password: {}'.format(username, user_password))
        else
            print('create_admin_user() => unable to create admin user => username, password: {}'.format(username, user_password))

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

