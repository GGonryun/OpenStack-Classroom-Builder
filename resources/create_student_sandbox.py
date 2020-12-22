from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as k_client
import pandas as pd
import string
import random
import sys
import os
from hashlib import pbkdf2_hmac
import binascii
import argparse
import pprint
import users_utility
from create_student_users import create_single_user

### REQUIREMENTS ###
# Script requires you have loaded in the required variables to log into the CLI
# Script requires a csv file that is located in the same directory.
# CSV file must have non-nullable columns: Username, Project
# Admin user must exist in the 'admin' project with an admin role

## How to run: ##
#  python create_student_users.py -admin-username <username> -csv-filename <file.csv>

### Description ###
# Create student user sandbox projects given a csv file with a non-nullable Username column and non nullable Project column.
# It will add the given admin user if they exist and are an admin. Otherwise, defaults to adding the 'admin' user.
# It then adds the student to their sandbox project

def create_user_sandbox(username, admin_username):
    '''
    Create project and group, then adds group to project with student role
    '''
    print('create_user_sandbox(username: {}, admin_username: {})'.format(username, admin_username))
    keystone = users_utility.create_keystone_client()
    sandbox_name = 'Sandbox-' + username
    # Check if project exists
    project_id = users_utility.get_a_projectID(sandbox_name)
    does_sandbox_exist = project_id is not None
    print('create_user_sandbox() => does sandbox exist? {}'.format(does_sandbox_exist))
    if not does_sandbox_exist:
        project_id = keystone.projects.create(sandbox_name, 'default').id
    
    # add specified admin user to student sandbox
    add_admin_to_project(admin_username, project_id)
    print('create_user_sandbox() => finished creating sandbox'.format(project_id))
    return project_id


def add_admin_to_project(admin_username, project_id):
    '''
    Adds admin user to student sandbox project, Otherwise defaults to adding 'admin' user
    '''
    print('add_admin_to_project(admin_username: {}, project_id: {})'.format(admin_username, project_id))

    is_admin = users_utility.is_admin(admin_username)
    print('add_admin_to_project(admin_username: {}) => is_admin ? {}'.format(admin_username, is_admin))
    # Check if admin they gave me is actually an admin
    if users_utility.is_admin(admin_username):
        user = users_utility.get_user(admin_username)
        # add them to user project
        users_utility.add_user_to_project(users_utility.ADMIN_ROLE, project_id, user)
    else:
        # add default 'admin' user to project
        users_utility.add_user_to_project(users_utility.ADMIN_ROLE, project_id, users_utility.ADMIN_USER)
    print('add_admin_to_project(admin_username: {}) => finihed adding admin to project {}'.format(admin_username, project_id))


def create_project_per_student(rows, admin_username):
    '''
    Creates a sandbox project for each user in the CSV file.
    '''
    print("create_project_per_student(rows, admin_username: {})".format(admin_username))
    for row in rows:
        username = row['Username']
        project_id = create_user_sandbox(username, admin_username)
        user = users_utility.get_user(username)
        does_user_exist = user is not None
        print("create_project_per_student()=> username: {} => does user exist ?".format(username, does_user_exist))
        if does_user_exist:
            users_utility.add_user_to_project(users_utility.STUDENT_ROLE, project_id, user)
        else:
            user = create_single_user(row, project_id)
            users_utility.add_user_to_project(users_utility.STUDENT_ROLE, project_id, user)
        print("create_project_per_student() => username: {} => finished creating user and adding to project".format(username))
        
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-admin-username", help="The username of the admin you want added to the student projects.")
    parser.add_argument("-csv-file", dest='csvfile', required=True, help='The csv file that holds the students Username', type=file)
    args = parser.parse_args()

    if args.admin_username:
        csv_filename = args.csvfile.name
        # Read CSV file
        student_dataframe = pd.read_csv(csv_filename)
        rows = student_dataframe.T.to_dict().values()
        for row in rows:
            row['Password'] = users_utility.generate_user_password(row['Username'])
        create_project_per_student(rows, args.admin_username)
        pprint.pprint(rows)
    else:
        raise Exception('create_student_sandbox.py usage: -admin-username <username> <CSV-FILE>')
