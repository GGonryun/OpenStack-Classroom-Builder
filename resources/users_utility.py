from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as k_client
from novaclient import client as n_client
from neutronclient.v2_0 import client as e_client
import string
import random
import sys
import os
from hashlib import pbkdf2_hmac
import binascii
import pprint

# Resource: https://docs.openstack.org/python-keystoneclient/latest/api/keystoneclient.v3.html#keystoneclient.v3.roles.RoleManager

### Utility Class for Keystone.Identity API ###
# Holds frequently used functions working when with Keystone client api
# Has utility function that will create an authenticated keystone client, using env variables
# As of 10/2020 This utility class only works with the 'Default' domain

### INSTRUCTIONS ###
# import this module where needed

#### USER DEFINED CONSTANT ####
OS_PASSWORD = 'OS_PASSWORD'
OS_USERNAME = 'OS_USERNAME'
OS_PROJECT = 'OS_PROJECT_NAME'
OS_PROJECT_DOMAIN = 'OS_PROJECT_DOMAIN_NAME'
OS_AUTH_URL = 'OS_AUTH_URL'
OS_USER_DOMAIN = 'OS_USER_DOMAIN_NAME'
NOVA_API_VERSION = 2


def env(name):
    '''
    Utility function to access environment variables
    '''
    if name in os.environ:
        return os.environ[name]
    else:
        raise Exception('{} does not exist as an environment variable', format(name))


def create_keystone_client():
    '''
    Utility function that creates an authenticated keystone client.
    Uses environment variables.
    '''
    auth = v3.Password(auth_url=env(OS_AUTH_URL),
                       username=env(OS_USERNAME),
                       password=env(OS_PASSWORD),
                       project_name=env(OS_PROJECT),
                       user_domain_name=env(OS_USER_DOMAIN),
                       project_domain_name=env(OS_PROJECT_DOMAIN))

    sess = session.Session(auth=auth)
    keystone = k_client.Client(session=sess)
    return keystone


def create_nova_client(username, password, project, domain):
    '''
    The nova client operates on VM's specific to a users account.
    Uses environment variables.
    '''
    auth = v3.Password(auth_url=env(OS_AUTH_URL),
                      username=username,
                      password=password,
                      project_name=project,
                      user_domain_name=domain,
                      project_domain_name=domain)
    session = session.Session(auth=auth)
    return n_client.Client(NOVA_API_VERSION, session=session)


def create_neutron_client(project, domain):
    '''
    The neutron client operates at the project-level and uses 
    environment variables for an admin account.
    You must first add the admin account before modifying 
    a project's network resources.
    '''
    auth = v3.Password(auth_url=env(OS_AUTH_URL),
                      username=env(OS_USERNAME),
                      password=env(OS_PASSWORD),
                      project_name=project,
                      user_domain_name=domain,
                      project_domain_name=domain)
    session = session.Session(auth=auth)
    return e_client.Client(session=session)


def get_user(username):
    '''
    Get a user by username
    '''
    keystone = create_keystone_client()
    users = keystone.users.list(domain='default')
    for user in users:
        if user.name == username:
            return user
    print('Could not find a user with the username: ' + username)
    return None


def get_role(name):
    keystone = create_keystone_client()
    roles = keystone.roles.list(domain='default')
    for role in roles:
        if role.name == name:
            return role
    print('Error, could not find role with name: ' + name)
    return None 


# Frequently used roles
ADMIN_ROLE = get_role('admin')
PROFESSOR_CHUCK = get_user('cbane3')
ADMIN_USER = get_user('admin')
STUDENT_ROLE = get_role('Student')


def get_projects():
    '''
    Get a dictionary of projects in the default domain.
    The key is the projects' name and the value is the projects' id
    '''
    keystone = create_keystone_client()
    projects = keystone.projects.list(domain='default')
    # Using dictionary comprehension to build a dictionary of each project and their ids
    project_dict = { project.name : project.id for project in projects }
    return project_dict


def get_a_projectID(name):
    project_dict = get_projects()
    project_ID = project_dict.get(name, None)
    return project_ID


def get_a_project(project_name):
    print("\tget_a_project(project_name): {}".format(project_name))
    try:
        keystone = create_keystone_client()
        projz = keystone.projects.list()
        projects = filter(lambda p : p.name == project_name, projz)
        numProjects = len(projects)
        print("projects found: {}".format(projects))
        return projects[1]
    except:
        print("unable to find project: {}".format(project_name))
        return None


def add_user_to_project(role, project_id, user):
    '''
    Requires a role to be granted to user.
    role: the role to be granted 
    project_id: the project in which the role will be granted
    user: user to have role granted on a resource
    '''
    keystone = create_keystone_client()
    keystone.roles.grant(role, project=project_id, user=user)


def get_groups():
    '''
    Get a dictionary of groups in the default domain.
    They key is the groups' name and the value is the groups' id.
    '''
    keystone = create_keystone_client()
    groups = keystone.groups.list(domain='default')
    groups_dict = { group.name : group.id for group in groups }
    return groups_dict


def get_a_groupID(name):
    groups_dict = get_groups()
    group_ID = groups_dict.get(name, None)
    return group_ID


def add_user_to_group(user, group_id):
    keystone = create_keystone_client()
    keystone.users.add_to_group(user=user.id, group=group_id)


def create_single_user(username, user_password, project_id, role):
    '''
     Create an enabled single user in the 'default' domain.

     In order for the user to be able to sign in they must be added to a project by being
     given a role.
    '''
    keystone = create_keystone_client()
    user = keystone.users.create(name=username, domain='default', password=user_password,
                                 enabled=True, default_project=project_id)
    if user:
        # Add user to project
        add_user_to_project(role, project_id, user)
    else:
        raise Exception('Encountered an error creating user with name: ' + username)
    return user


def is_admin(username):
    '''
    Check if a user is an admin but checking their role
    and that they are part of the admin project
    '''
    keystone = create_keystone_client()
    admin_project = get_a_projectID('admin')
    user = get_user(username)
    if user:
        roles = keystone.roles.list(user=user, project=admin_project)
        for role in roles:
            if role.name == ADMIN_ROLE.name:
                return True
        else:
            print('User exists but does not have the admin role.')
    return False


def add_group_to_project(role, project_id, group_id):
    '''
    Creates an association between a group and a specific project.

    Any users added to the group will have access the projects associated with the group.
    '''
    keystone = create_keystone_client()
    keystone.roles.grant(role, project=project_id, group=group_id)


def generate_hash(salt, password):
    '''
    Generate a new password using the salt and users username

    Resource: https://docs.python.org/3/library/hashlib.html
    '''
    derived_key = pbkdf2_hmac('sha512', password, salt, 500)
    new_password = binascii.hexlify(derived_key)[0:9]
    return new_password


def generate_user_password(username):
    '''
    Generate user password.
    Result is a hash of their username and salt

    Resource: https://docs.python.org/3/library/hashlib.html
    '''
    user_password = generate_hash('plsnohack', username)
    return user_password
