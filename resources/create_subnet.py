import argparse
import sys
import users_utility

NAMESERVERS =  ['8.8.8.8', '8.8.4.4']

def create_subnet(domain, project, name, network_id=None, cidr=None):
  '''
    returns the subnet object
    an id can be used to find the subnet instead of the name.
  '''
  
  print("create_subnet(domain, project, name, network_id, cidr): {}, {}, {}, {}, {}".format(domain, project, name, network_id, cidr))
  client = users_utility.create_neutron_client(domain, project)

  subnet = find_subnet(client, name)
  if subnet:
    print("create_subnet: found subnet:", subnet)
    return subnet
  else:
    response = client.create_subnet({'subnet': {'name': name, 'network_id': network_id, 'ip_version': 4, 'cidr': cidr, 'dns_nameservers': NAMESERVERS }})
    print("subnet: {}".format(response))
    return response['subnet']


def find_subnet(client, name):
  print('find_subnet(client, name):', client, name)
  subnets = list(filter(lambda s : s['name'] == name or s['id'] == name, client.list_subnets()['subnets']))
  numSubnets = len(subnets)

  print('find_subnet: numSubnets:', numSubnets)
  if numSubnets == 1:
    return subnets[0]
  
  return None

#run: 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="name of domain for the subnet")
    parser.add_argument("--project", help="name project for the subnet")
    parser.add_argument("--name", help="name to give subnet")
    parser.add_argument("--network-id", help="the network id the subnet belongs to")
    parser.add_argument("--cidr", help="the ip address range ex: 192.168.199.0/24")
    args = parser.parse_args()

    if args.domain and args.project and args.name and args.network_id and args.cidr:
        create_subnet(args.domain, args.project, args.name, args.network_id, args.cidr)
    else:
        raise Exception('create_subnet.py usage: --domain <string> --project <string> --name <string> --network_id <string> --cidr <string>')
