import argparse
import sys
import pprint
import users_utility

STUDENTS = 'Students'
DOMAIN = 'Domain'
PROJECT = 'Project'
NETWORKS = 'Networks'
USERNAME = 'Username'
PASSWORD = 'Password'
NAME = 'Name'
IMAGE = 'Image'
FLAVOR = 'Flavor'
INSTANCES = 'Instances'


def create_student_machine(ledger, machine): 
  print('create_student_machine(ledger, machine): {}, {}'.format(ledger, machine))
  for student in ledger[STUDENTS]:
    instances = machine[INSTANCES]
    print('create_student_machine: machine, student, instances: {}, {}, {}'.format(machine, student, instances))
    for num in range(0, int(instances)):
      n = num + 1
      name = username + "-" + machine[NAME] + "-" + str(n)
      return create_machine(ledger[DOMAIN].name, ledger[PROJECT].name, student[USERNAME], student[PASSWORD], name, machine[IMAGE], machine[FLAVOR], ledger[NETWORKS][ID])


def create_project_machine(ledger, machine):
  instances = machine[INSTANCES]
  print('create_project_machine: machine, instances: {}, {}'.format(machine, instances))
  for num in range(0, int(instances)):
    n = num + 1
    project = ledger[PROJECT].name
    name = project + "-" + machine[NAME] + "-" + str(n)
    return create_machine(ledger[DOMAIN].name, project, student[USERNAME], student[PASSWORD], name, machine[IMAGE], machine[FLAVOR], ledger[NETWORKS][ID])


def create_machine(domain, project, username, password, name, image, flavor, network_id):
  print("create_machine(domain, project, username, password, name, image, flavor, network_id):", domain, project, username, password, name, image, flavor, network_id)
  
  try:
    client = users_utility.get_nova_client(username, password, domain, project)
    return client.servers.create(name=name, image=image, flavor=flavor, nics=[{ 'net-id': network_id }])
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