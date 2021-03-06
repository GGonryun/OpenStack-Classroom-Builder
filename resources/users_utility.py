from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as k_client
from novaclient import client as n_client
from neutronclient.v2_0 import client as e_client
from glanceclient.v2 import client as g_client
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

keystone_session = None
def create_keystone_client():
    '''
    Utility function that creates an authenticated keystone client.
    Uses environment variables.
    '''
    global keystone_session
    if keystone_session == None:
        auth = v3.Password(auth_url=env(OS_AUTH_URL),
                        username=env(OS_USERNAME),
                        password=env(OS_PASSWORD),
                        project_name=env(OS_PROJECT),
                        user_domain_name=env(OS_USER_DOMAIN),
                        project_domain_name=env(OS_PROJECT_DOMAIN))

        keystone_session = session.Session(auth=auth)

    keystone = k_client.Client(session=keystone_session)
    return keystone


nova_session = {}
def create_nova_client(username, password, domain, project):
    '''
    The nova client operates on VM's specific to a users account.
    Uses environment variables.
    '''
    global nova_session
    username = username if username else env(OS_USERNAME)
    password = password if password else env(OS_PASSWORD)
    key = username + domain + project
    if(key not in nova_session):
        auth = v3.Password(auth_url=env(OS_AUTH_URL),
                        username=username,
                        password=password,
                        project_name=project,
                        user_domain_name=domain,
                        project_domain_name=domain)
        nova_session[key] = session.Session(auth=auth)

    return n_client.Client(NOVA_API_VERSION, session=nova_session[key])


neutron_session = {}
def create_neutron_client(domain, project):
    '''
    The neutron client operates at the project-level and uses 
    environment variables for an admin account.
    You must first add the admin account before modifying 
    a project's network resources.
    '''
    global neutron_session
    key = domain + project
    if(key not in neutron_session):
        auth = v3.Password(auth_url=env(OS_AUTH_URL),
                        username=env(OS_USERNAME),
                        password=env(OS_PASSWORD),
                        project_name=project,
                        user_domain_name=domain,
                        project_domain_name=domain)
        neutron_session[key] = session.Session(auth=auth)

    return e_client.Client(session=neutron_session[key])


glance_session = None
def create_glance_client():
    '''
    The neutron client operates at the project-level and uses 
    environment variables for an admin account.
    You must first add the admin account before modifying 
    a project's network resources.
    '''
    global glance_session
    if(glance_session == None):
        auth = v3.Password(auth_url=env(OS_AUTH_URL),
                        username=env(OS_USERNAME),
                        password=env(OS_PASSWORD),
                        project_name=env(OS_PROJECT),
                        user_domain_name=env(OS_USER_DOMAIN),
                        project_domain_name=env(OS_USER_DOMAIN))
        glance_session = session.Session(auth=auth)
    return g_client.Client(session=glance_session)


def get_user(username):
    '''
    Get a user by username
    '''
    keystone = create_keystone_client()
    users = keystone.users.list(domain='default')
    for user in users:
        if user.name == username:
            print('get_user(username: {}): => found user'.format(username))
            return user
    print('get_user(username: {}) => could not find user'.format(username))
    return None


def get_role(name):
    keystone = create_keystone_client()
    roles = keystone.roles.list(domain='default')
    for role in roles:
        if role.name == name:
            print('get_role(name: {}): => found role'.format(name))

            return role
    print('get_role(name: {}): => could not find role'.format(name))
    return None 

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
    print('get_a_projectID(name: {}) => id: {}'.format(name, project_ID))
    return project_ID


def get_a_project(project_name):
    try:
        keystone = create_keystone_client()
        projects = list(filter(lambda p : p.name == project_name, keystone.projects.list()))
        numProjects = len(projects)
        if(numProjects > 0):
            project = projects[0]
            print("get_a_project(project_name: {}) found project".format(project_name))
            return project
        
    except Exception as ex:
        print("unable to find project: {}, {}".format(ex, project_name))
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
    print('add_user_to_project(project_id: {}, role: {}) => finished adding user to project'.format(project_id, role))


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
    print('get_a_groupID(name: {}) => id {}'.format(name, group_ID))

    return group_ID


def add_user_to_group(user, group_id):
    keystone = create_keystone_client()
    keystone.users.add_to_group(user=user.id, group=group_id)
    print('add_user_to_group(user, group_id: {}) => finished adding user to group'.format(group_id))


def create_single_user(username, user_password, project_id, role):
    '''
     Create an enabled single user in the 'default' domain.

     In order for the user to be able to sign in they must be added to a project by being
     given a role.
    '''
    print('create_single_user(username: {}, user_password: <HIDDEN>, project_id: {}, role: {})'.format(username, project_id, role))
    keystone = create_keystone_client()
    user = keystone.users.create(name=username, domain='default', password=user_password,
                                 enabled=True, default_project=project_id)
    if user:
        # Add user to project
        add_user_to_project(role, project_id, user)
    else:
        raise Exception('Encountered an error creating user with name: ' + username)
    print('create_single_user() => finished creating new user: {}'.format(username))
    return user


def is_admin(username):
    '''
    Check if a user is an admin but checking their role
    and that they are part of the admin project
    '''
    keystone = create_keystone_client()
    admin_project = get_a_projectID('admin')
    user = get_user(username)
    success = false
    if user:
        roles = keystone.roles.list(user=user, project=admin_project)
        for role in roles:
            if role.name == ADMIN_ROLE.name:
                success = True
    
    print('is_admin(admin: {}) => ? {}'.format(username, admin))
    return success


def add_group_to_project(role, project_id, group_id):
    '''
    Creates an association between a group and a specific project.

    Any users added to the group will have access the projects associated with the group.
    '''
    print('add_group_to_project(role: {}, project_id {}, group_id {})'.format(role, project_id, group_id))
    keystone = create_keystone_client()
    keystone.roles.grant(role, project=project_id, group=group_id)
    print('add_group_to_project(role: {}, project_id {}, group_id {}) => success'.format(role, project_id, group_id))


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

# Frequently used roles
ADMIN_ROLE = get_role('admin')
PROFESSOR_CHUCK = get_user('cbane3')
ADMIN_USER = get_user('admin')
STUDENT_ROLE = get_role('student')
