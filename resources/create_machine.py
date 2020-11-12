import argparse
import sys
import pprint
import users_utility
import create_network

STUDENTS = 'Students'
DOMAIN = 'Domain'
PROJECT = 'Project'
NETWORK = 'Network'
USERNAME = 'Username'
PASSWORD = 'Password'
NAME = 'Name'
IMAGE = 'Image'
FLAVOR = 'Flavor'
INSTANCES = 'Instances'
ID = 'id'


def create_student_machine(ledger, machine): 
  m = []
  for student in ledger[STUDENTS]:
    print('create_student_machine(ledger, machine, student)', ledger, machine, student)
    instances = machine[INSTANCES]
    for num in range(int(instances)):
      i = num + 1
      username = student[USERNAME]
      name = username + "-" + machine[NAME] + "-" + str(i)
      n = create_network.create_network(ledger[DOMAIN].name, ledger[PROJECT].name, machine[NETWORK])
      m.append(create_machine(ledger[DOMAIN].name, ledger[PROJECT].name, username, student[PASSWORD], name, machine[IMAGE], machine[FLAVOR], machine[PASSWORD], n['id']))
  return m


def create_project_machine(ledger, machine):
  print('create_project_machine(ledger, machine)', ledger, machine)
  m = []
  instances = machine[INSTANCES]
  for num in range(int(instances)):
    i = num + 1
    project = ledger[PROJECT].name
    name = project + "-" + machine[NAME] + "-" + str(i)
    n = create_network.create_network(ledger[DOMAIN].name, ledger[PROJECT].name, machine[NETWORK])
    m.append(create_machine(ledger[DOMAIN].name, project, None, None, name, machine[IMAGE], machine[FLAVOR], machine[PASSWORD], n['id']))
  return m


def get_flavor_id(client, flavor_name):
  print('get_flavor_id(client, flavor_name)', client, flavor_name)
  f = client.flavors.list()
  flavor = list(filter(lambda f : f.name == flavor_name, f))

  n = len(flavor)
  if n == 1:
    return flavor[0].id
  else:
    raise Exception('invalid flavor name', flavor_name)


def get_image_id(image_name):
  print('get_image_id(image_name)', image_name)
  client = users_utility.create_glance_client()
  images = client.images.list()
  image = list(filter(lambda i : i.name == image_name, images))

  if len(image) == 1:
    return image[0]['id']
  else:
    raise Exception('cannot find image', image)


def create_machine(domain, project, username, password, name, image, flavor, machine_pass, network_id):
  print("create_machine(domain, project, username, password, name, image, flavor, machine_pass, network_id):", domain, project, username, password, name, image, flavor, machine_pass, network_id)
  
  try:
    client = users_utility.create_nova_client(None, None, domain, project)
    # flavor names must be lowercase, this convention is enforced in openstack, all our flavor names are lower-case only.
    f = get_flavor_id(client, flavor.lower())
    i = get_image_id(image)
    # This ID is for Windows 10 Pro
    if(i == '49b579ed-37fc-47fc-87b8-e35ff62407e4'):
      return client.servers.create(name=name, image=i, flavor=f, nics=[{ 'net-id': network_id }], meta={ 'admin_pass': 'Password1234' })
    # This ID is the windows 2016 server image on OpenStack.
    elif(i == '847463d2-b7f6-4ed7-979a-8ed9301ce0c4'):
      # We should specify the appropriate availibility_zone for windows server 2016 images.
      return client.servers.create(availability_zone='win', name=name, image=i, flavor=f, nics=[{ 'net-id': network_id }], meta={ 'admin_pass': 'Password1234' })
    else:
      return client.servers.create(name=name, image=i, flavor=f, nics=[{ 'net-id': network_id }])
  except Exception as ex:
    return "an error has occured creating machine {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(ex, domain, project, username, password, name, image, flavor, machine_pass, network_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="domain to create machine in.")
    parser.add_argument("--project", help="project to create machine in.")
    parser.add_argument("--username", help="user to create machine for.")
    parser.add_argument("--password", help="password for user.")
    parser.add_argument("--name", help="display name for machine.")
    parser.add_argument("--image", help="the type of operating system or snapshot to deploy machine with.")
    parser.add_argument("--flavor", help="the size of the machine.")
    parser.add_argument("--network_id", help="the network attached to the machine.")
    args = parser.parse_args()

    if args.domain and args.project and args.username and args.password and args.name and args.image and args.flavor and args.network_id:
        create_machine(args.id)
    else:
        raise Exception('get_domain.py incorrect usage')