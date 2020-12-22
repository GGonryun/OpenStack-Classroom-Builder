from keystoneauth1.identity import v3
from keystoneauth1 import session
import sys
import os
from hashlib import pbkdf2_hmac
import binascii
import argparse
import pprint
from keystoneclient.v3 import client as k_client
import users_utility

 ### REQUIREMENTS ###
# This script assumes you have loaded in the required variables to log into the CLI.

## Description ##
# Create a project with user and role of choice. If --show-password flag with username is given then it will check if
# that user exists and show their initial password.
# The domain is hard-coded to 'Default'

# How to run #
# python create_project.py --project-name <name> --username <name> --role <role>
# python create_project.py --show-password <username>


def create_project(project_name, username, user_role):
    print('create_project(project_name: {}, username: {}, user_role: {})'.format(project_name, username, user_role))
    keystone = users_utility.create_keystone_client()

    # Do a quick check if project exists
    project = users_utility.get_a_project(project_name)
    does_project_exist = project is not None
    print('create_project(project_name: {}) => does project exist ? {}'.format(does_project_exist))
    if not does_project_exist:
        project = keystone.projects.create(project_name, 'default')
    print('create_project(project_name: {}) => using project: {}'.format(project))

    # check if role exists and create it if it doesn't
    role = users_utility.get_role(user_role)
    does_role_exist = role is not None
    print('create_project(user_role: {}) => does role exist ? {}'.format(project_name, user_role, does_role_exist))
    if not does_role_exist:
        role = keystone.roles.create(name=user_role)
    print('create_project(user_role: {}) => using role {}'.format(user_role, does_role_exist))
    # add user to project
    user = users_utility.get_user(username)


    does_user_exist = user is not None
    print('create_project(username: {}) => does user exist ? {}'.format(username, does_user_exist))
    if does_user_exist:
        project_id = project.id if project != None else None
        users_utility.add_user_to_project(role, project_id, user)
    else:
        user_password = users_utility.generate_user_password(username)
        users_utility.create_single_user(username, user_password, project_id, role)
        
    print('create_project(user_role: {}) => added user to project {} with id: {}'.format(username, project_name, project_id))
    return project


#run: 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-name", help="Name that will belong to project")
    parser.add_argument("--username", help="User that will be added to project")
    parser.add_argument("--role", help="Role that user will have in project")
    parser.add_argument("--show-password", help="Show the newly created users password")
    args = parser.parse_args()

    if args.project_name and args.username and args.role:
        create_project(args.project_name, args.username, args.role)
    elif args.show_password:
        # show initial password for given username
        user = get_user(args.show_password)
        if user:
            password = users_utility.generate_user_password(args.show_password)
            pprint.pprint('User: ' + args.show_password + ' password: ' + password)
        else:
            raise Exception('User does not exist!')
    else:
        raise Exception('create_project.py usage: --project-name <name> --username <username> --role <role> or --show-password <username>')
