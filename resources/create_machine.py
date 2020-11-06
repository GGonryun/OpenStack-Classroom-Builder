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
  print('create_student_machine(ledger, machine): {}, {}'.format(ledger, machine))
  for student in ledger[STUDENTS]:
    instances = machine[INSTANCES]
    print('create_student_machine: machine, student, instances: {}, {}, {}'.format(machine, student, instances))
    for num in range(0, int(instances)):
      i = num + 1
      username = student[USERNAME]
      name = username + "-" + machine[NAME] + "-" + str(i)
      n = create_network.create_network(ledger[DOMAIN].name, ledger[PROJECT].name, machine[NETWORK])
      return create_machine(ledger[DOMAIN].name, ledger[PROJECT].name, username, student[PASSWORD], name, machine[IMAGE], machine[FLAVOR], n['id'])


def create_project_machine(ledger, machine):
  print('create_project_machine: ledger:', ledger)
  instances = machine[INSTANCES]
  print('create_project_machine: machine, instances: {}, {}'.format(machine, instances))
  for num in range(0, int(instances)):
    i = num + 1
    project = ledger[PROJECT].name
    name = project + "-" + machine[NAME] + "-" + str(i)
    n = create_network.create_network(ledger[DOMAIN].name, ledger[PROJECT].name, machine[NETWORK])
    return create_machine(ledger[DOMAIN].name, project, None, None, name, machine[IMAGE], machine[FLAVOR], n['id'])


def get_flavor_id(client, flavor_name):
  f = client.flavors.get(flavor_name)
  print('found flavors', f)
  if f:
    return f
  else:
    raise Exception('invalid flavor name', flavor_name)

def get_image_id(client, image_name):
  image = client.images.find_image(image_name)
  print('found image', image)

  if image:
    return image.id
  else:
    raise Exception('cannot find image', image)

def create_machine(domain, project, username, password, name, image, flavor, network_id):
  print("create_machine(domain, project, username, password, name, image, flavor, network_id):", domain, project, username, password, name, image, flavor, network_id)
  
  try:
    client = users_utility.create_nova_client(None, None, domain, project)
    f = get_flavor_id(client, flavor)
    i = get_image_id(client, image)
    return client.servers.create(name=name, image=i, flavor=f, nics=[{ 'net-id': network_id }])
  except Exception as ex:
    print("an error has occured creating machine {}, {}, {}, {}, {}, {}, {}, {}, {}".format(ex, domain, project, username, password, name, image, flavor, network_id))
    return None


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