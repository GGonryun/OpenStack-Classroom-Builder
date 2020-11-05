import argparse
import sys
import users_utility


def create_router(domain, project, name, network_id, subnet_id, ip_address):
  '''
  ip_address = the ip address to attach the router to.
  subnet_id = when connecting to external services use `939dfc59-9c31-42fe-8cfa-78d2838b5b76` which is currently the external provider network's subnet id.
  '''
  print('\tcreate_router(domain, project, name, network_id, subnet_id, ip_address): {}, {}, {}, {}, {}, {}'.format(domain, project, name, network_id, subnet_id, ip_address))
  try:
    client = users_utility.create_neutron_client(domain, project)
    external_fixed_ips = [{'ip_address': ip_address, 'subnet_id': subnet_id}]
    external_gateway_info = { 'network_id': network_id, 'enable_snat': True, 'external_fixed_ips': external_fixed_ips}
    network = client.create_router({'router': {'name': name, 'admin_state_up': True, 'external_gateway_info': external_gateway_info}})
    return network.id
  except Exception as ex:
      pprint.pprint("\tcreate_router: an error has occured {}, {}, {}, {}, {}, {}, {}", ex, domain, project, name, network_id, subnet_id, ip_address)

#run: 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="name of domain for the router")
    parser.add_argument("--project", help="name of project for the router")
    parser.add_argument("--name", help="name for the router")
    parser.add_argument("--network-id", help="the external network to connect to should be a guid such as: '939dfc59-9c31-42fe-8cfa-78d2838b5b76'")
    parser.add_argument("--subnet-id", help="the subnet to connect to should be a guid and attached to the network above. ")
    parser.add_argument("--ip", help="an ip address on the subnet_id.")
    args = parser.parse_args()

    if args.domain and args.project and args.name and args.network_id and args.subnet_id and args.ip:
        create_router(args.domain, arg.project, args.name, args.network_id, args.subnet_id, args.ip)
    else:
        raise Exception('create_router.py incorrect usage')