import argparse
import create_subnet
import create_router
import users_utility
import random

NAME = 'Name'
CIDR = 'Subnet'
PROVIDER = 'Provider'
USERNAME = 'Username'
EXTERNAL = 'External'

def create_linked_network(domain, project, network):
  ln = []
  print('create_linked_network(domain: {}, project: {}, network: {})'.format(domain, project, network))
  external = network[EXTERNAL] if network[EXTERNAL] != None else False
  domain_name = domain.name
  project_name = project.name
  # The sequence of steps is important, we must first create the network [n], then the subnet [s].
  # afterwards we get the provider network [p], and the provider networks subnet [b].
  # we then select an ip-address on the provider subnet's ip address range.
  # finally you can create a router using all the pieces that links your new network to the external network.
  n = create_network(domain_name, project_name, network[NAME], external)
  s = create_subnet.create_subnet(domain_name, project_name, network[NAME], n['id'], network[CIDR])
  p = create_network(domain_name, project_name, network[PROVIDER])
  i = p['subnets'][0]
  b = create_subnet.create_subnet(domain_name, project_name, i)
  a = select_ip(b['cidr'], b['allocation_pools'])
  k = network[PROVIDER] + "-Router"
  r = create_router.create_router(domain_name, project_name, k, p['id'], i, a, s['id'])
  ln.append(n)
  return ln

def create_network(domain, project, name, is_external=False):
  '''
  attempts to find a given network by name inside of a project, if the network is found we return it.
  otherwise we create a new network.
  '''

  print('create_network(domain, project, name, is_external)', domain, project, name, is_external)
  try:
    client = users_utility.create_neutron_client(domain, project)
    # find network:
    netz = client.list_networks()['networks']
    networks = list(filter(lambda a : a['name'] == name, netz))
    numNetworks = len(networks)

    print('create_network: networks found {}'.format(numNetworks))
    if numNetworks == 1:
      return networks[0]
    elif numNetworks == 0:
      return client.create_network({'network': {'name': name, 'admin_state_up': True, 'router:external': is_external}})['network']
    else:
      return None

  except Exception as ex:
      print("an error occured getting the network", ex, domain, project, name, is_external)


def select_ip(cidr, allocation_pools):
  print('select_ip(cidr, allocation_pools):', cidr, allocation_pools)
  ar = cidr.split('/')
  ip = ar[0]
  rg = ar[1]
  c = ip.split('.')
  print('select_ip: ip, r', ip, rg)

  if (rg == '24'): #subnet range /24 means the last value 0 can be replaced with any value within 0-255
    v = 0
    if(allocation_pools and len(allocation_pools) == 1):
      start, end = get_ip_range(allocation_pools[0])
      v = random.randint(start, end)
    else:
      v = random.randint(0,256)
    return c[0] + "." + c[1] + "." + c[2] + "." + str(v)
  else:
    return c[0] + "." + c[1] + "." + c[2] + "." + "?"
    

def get_ip_range(allocation_pool):
  print('get_ip_range(allocation_pool)', allocation_pool)
  start = allocation_pool['start'].split('.')[-1]
  end = allocation_pool['end'].split('.')[-1]
  return (int(start), int(end) + 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="name of domain for network")
    parser.add_argument("--project", help="name of project for network")
    parser.add_argument("--name", help="name of network")
    parser.add_argument("--external", help="adding this flag allows the current network to provide a connection to other networks")
    args = parser.parse_args()

    if args.domain and args.project and args.name:
      external = True if args.external else False
      print(create_network(args.domain, args.project, args.name, external))
    else:
        raise Exception('create_network.py usage: --domain <name> --project <name> --name <name> [--external]')