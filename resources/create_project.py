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
    created_project = {}
    keystone = users_utility.create_keystone_client()
    project_name = project_name
    # Do a quick check if project exists
    project = users_utility.get_a_project(project_name)
    project_id = project.id if project != None else None

    if project_id:
        print('Project with name: ' + project_name + ' and id: ' + project_id + ' already exists. ...Continuing Script...')
    else:
        print("...Creating Project...")
        project = keystone.projects.create(project_name, 'default')
        project_id = project.id

    # check if role exists and create it if it doesn't
    role = users_utility.get_role(user_role)
    if role:
        # Do nothing this is great
        print(role)
    else:
        print('Creating new role with the name: ' + user_role)
        role = keystone.roles.create(name=user_role)
    # add user to project
    user = users_utility.get_user(username)
    if user:
        users_utility.add_user_to_project(role, project_id, user)
    else:
        print("Creating user with the username: " + username)
        user_password = users_utility.generate_user_password(username)
        users_utility.create_single_user(username, user_password, project_id, role)
        print("...Adding user to project ...")

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
