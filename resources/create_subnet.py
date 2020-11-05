import argparse
import sys
import users_utility


def create_subnet(domain, project, name, network_id, cidr):
  '''
    returns the id
  '''
  print("\tcreate_subnet(domain, project, name, network_id, cidr): {}, {}, {}, {}, {}".format(domain, project, name, network_id, cidr))
  try:
    client = users_utility.get_neutron_client(domain, project)
    subnet = client.create_subnet({'subnet': {'name': name, 'network_id': network_id, 'ip_version': 4, 'cidr': cidr, 'dns_nameservers': ['8.8.8.8', '8.8.4.4']}})
    return subnet.id
  except Exception as ex:
      print("\tcreate_subnet: an error occured:, {}, {}, {}, {}, {}", ex, domain, project, user, network)

#run: 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="name of domain for the subnet")
    parser.add_argument("--project", help="name project for the subnet")
    parser.add_argument("--name", help="name to give subnet")
    parser.add_argument("--network_id", help="the network id the subnet belongs to")
    parser.add_argument("--cidr", help="the ip address range ex: 192.168.199.0/24")
    args = parser.parse_args()

    if args.domain and args.project and args.name and args.network_id and args.cidr:
        create_subnet(args.domain, args.project, args.name, args.network_id, args.cidr)
    else:
        raise Exception('create_subnet.py usage: --domain <string> --project <string> --name <string> --network_id <string> --cidr <string>')
