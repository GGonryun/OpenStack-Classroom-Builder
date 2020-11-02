from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as k_client
from novaclient import client as n_client
from neutronclient.v2_0 import e_client
import os

##### USER DEFINED CONSTANT #####
AUTH_URL = "http://controller:5000/v3"
OS_PASSWORD = 'OS_PASSWORD'
OS_USERNAME = 'OS_USERNAME'
OS_PROJECT = 'OS_PROJECT_NAME'
OS_PROJECT_DOMAIN = 'OS_PROJECT_DOMAIN_NAME'
OS_USER_DOMAIN = 'OS_USER_DOMAIN_NAME'
NOVA_API_VERSION = 2
USERNAME_KEY = "Username"
PASSWORD_KEY = "Password"
NAME_KEY = "Name"
IMAGE_KEY = "Image_ID"
FLAVOR_KEY = "Flavor_ID"
NETWORK_KEY = "Network_ID"
EXTERNAL_KEY = "External"

def env(name):
    if name in os.environ:
        return os.environ[name]
    else:
        raise Exception('{} does not exist as an environment variable!'.format(name))

# user = { username, password }
# machine = { name, instances, image_id, flavor_id, network_id }

def get_domain(domain):
def get_project(project):
def get_student(domain, project, user):

def get_network(domain, project, user, network):
  try:
    client = get_neutron_client(user[USERNAME_KEY], user[PASSWORD_KEY], domain, project)
    network = client.create_network({'network': {'name': network[NAME_KEY], 'admin_state_up': True, 'router:external': network[EXTERNAL_KEY]}})
    return network.id
  except Exception ex:
      pprint.pprint("an error occured creating a network, {}, {}, {}, {}, {}", ex, domain, project, user, network)

def create_machine(domain, project, user, machine):
    try:
      client = get_nova_client(user[USERNAME_KEY], user[PASSWORD_KEY], domain, project)
      return client.servers.create(name=machine[NAME_KEY], image=machine[IMAGE_KEY], flavor=machine[FLAVOR_KEY], nics=[{ 'net-id': machine[NETWORK_KEY] }])
    except:
      pprint.pprint("an error has occured creating {}, {}, {}, {}, {}".format(username, vm_name, IMAGE_ID, FLAVOR_ID, NETWORK_ID))
      return None

def get_session(username, password, project, domain):
  auth = v3.Password(auth_url=AUTH_URL,
                     username=username,
                     password=password,
                     project_name=project,
                     user_domain_name=domain,
                     project_domain_name=domain)

  return session.Session(auth=auth)

def get_keystone_client(username, password, project, domain):
  return k_client.Client(session=get_session(username, password, project, domain))

def get_nova_client(username, password, project, domain):
  return n_client.Client(NOVA_API_VERSION, session=get_session(username, password, project, domain))

def get_neutron_client(username, password, project, domain):
  return e_client.Client(session=get_session(username, password, project, domain))