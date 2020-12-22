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

## REQUIREMENTS ##
# Script requires you have loaded in the required variables to log into the CLI
# Script requires a csv file that is located in the same directory.
# CSV file must have non-nullable columns: Username, Project
# Admin user must exist in the 'admin' project with an admin role

## Description ##
# This script creates users with the student role, in the default domain, and adds them to a group with the same name as the Project specified in the given CSV file.
# It also adds the given admin user, if they exist, if not it defaults to the 'admin' user

def create_student_users(rows, admin_username=None):
    '''
    Create users with student role and add to project based off 
    of the 'Project' column in the csv file
    '''
    print("create_student_users(rows: {}, admin_username: {})".format(rows, admin_username))
    keystone = users_utility.create_keystone_client()
    created_users = []
    for row in rows:
        users_project_name = row['Project']
        username = row['Username']
        project_id = users_utility.get_a_projectID(users_project_name)
        # check if user is an admin
        if project_id:
            print('create_student_users(users_project_name: {}) => found existing project with id: {}'.format(users_project_name, project_id))
        else:
            project_id = keystone.projects.create(users_project_name, 'default').id
            print('create_student_users(users_project_name: {}) => created new project with id: {}'.format(users_project_name, project_id))

        if admin_username:
            admin_user = users_utility.get_user(admin_username)
            is_admin = users_utility.is_admin(admin_username)
            print('create_student_users(admin_username: {}) => is user an admin? {}'.format(admin_username, is_admin))
            if is_admin:
                users_utility.add_user_to_project(users_utility.ADMIN_ROLE, project_id, admin_user)
            else:
                users_utility.add_user_to_project(users_utility.ADMIN_ROLE, project_id, users_utility.ADMIN_USER)
            print('create_student_users(admin_username: {}) => adding admin user to project {}'.format(admin_username, project_id))
          
        # Note: Group name must match 'Project' column name
        group_id = users_utility.get_a_groupID(users_project_name)
        # Check if group already exists
        has_existing_group = group_id is not None
        print('create_student_users() => does group exist? {}'.format(username, has_existing_group))
        if has_existing_group:
            users_utility.add_group_to_project(users_utility.STUDENT_ROLE, project_id, group_id)
        else:
            # Create the group
            group_id = keystone.groups.create(users_project_name, 'default').id
            users_utility.add_group_to_project(users_utility.STUDENT_ROLE, project_id, group_id)
        print('create_student_users() => finished adding group: {}, to project: {}'.format(group_id, project_id))

        ## Adding Users to group
        # get user
        # if user does not exist, create it
        user = users_utility.get_user(username)
        does_user_exist = user is not None
        print('create_student_users() => does username {} exist? {}'.format(username, does_user_exist))
        if not does_user_exist:
            user = create_single_user(row, project_id)
        added_user = add_user_to_group(username, group_id, row)
        print('create_student_users() => added username {} to group {}'.format(username, group_id))
        created_users.append(user)

    return created_users


def create_single_user(row, project_id):
    '''
    Create user with their default_project based on their project_name
    
    *Note: setting default_project does not add the user to the project.
            User must be added to a group that is associated to that project.
    '''
    print('create_single_user(row: {}, project_id: {})'.format(row, project_id))
    keystone = users_utility.create_keystone_client()
    username = row['Username']
    password = row['Password']
    user = users_utility.create_single_user(username, password, project_id, users_utility.STUDENT_ROLE)
    return user


def add_user_to_group(username, group_id, row):
    '''
    Add a single student user to their designated group
    which adds them to their designated project.
    '''
    user = users_utility.get_user(username)
    # check if user already exists
    if user:
        users_utility.add_user_to_group(user, group_id)
        print('add_user_to_group(username: {}, group_id: {}, row) => success'.format(username, group_id))
    else:
        raise Exception('User does not exist')
    return user


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-admin-username", help="The username of the admin you want added to the student projects.")
    parser.add_argument("-csv-filename", dest='csvfile', required=True, help='The csv file that holds the students Username and Project name', type=file)
    args = parser.parse_args()
    # run:
    if args.admin_username:
        csv_filename = args.csvfile.name
        # Read CSV file
        student_dataframe = pd.read_csv(csv_filename)
        rows = student_dataframe.T.to_dict().values()
        for row in rows:
            row['Password'] = users_utility.generate_user_password(row['Username'])
        create_student_users(rows, args.admin_username)
        pprint.pprint(rows)
    else:
        raise Exception('create_student_users.py usage: -admin-username <username> <CSV-FILENAME>')

    # if command == 'create-student-users':
    #     if args.admin-username:
    #         create_student_users()
    #     else:
    #         raise Exception('create_student_users.py usage: "create_student_users.py -admin-username <username> create-student-users <CSV-FILENAME>')
    # elif command == 'show-password':
    #     for row in rows:
    #         row['Password'] = generate_hash('plsnohack', row['Username'])
    #     pprint.pprint(rows)

