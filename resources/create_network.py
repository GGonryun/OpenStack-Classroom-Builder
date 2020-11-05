import argparse
import create_subnet
import create_router
import users_utility

NAME = 'Name'
CIDR = 'CIDR'
PROVIDER = 'Provider'
USERNAME = 'Username'
EXTERNAL = 'External'

def create_linked_network(domain, project, network):
  ln = []
  print('\tcreate_linked_network({}, {}, {})'.format(domain, project, network))
  external = network[EXTERNAL] if network[EXTERNAL] != None else False
  domain_name = domain.name
  project_name = project.name
  n = create_network(domain_name, project_name, network[NAME], external)
  s = create_subnet.create_subnet(domain_name, project_name, network[NAME], n.id, network[CIDR])
  p = create_network(domain_name, project_name, network[PROVIDER])
  ps = p['subnet'][0]
  a = select_ip(network[CIDR])
  r = create_router.create_router(domain_name, project_name, p.id, ps.id, a)
  ln.append(n)
  return ln

def create_network(domain, project, name, is_external):
  '''
  attempts to find a given network by name inside of a project, if the network is found we return it.
  otherwise we create a new network.
  '''
  print('\tcreate_network(domain, project, name, is_external)'.format(domain, project, name, is_external))
  try:
    client = users_utility.create_neutron_client(domain, project)
    # find network:
    networks = list(filter(lambda a : a.name == name, client.list_networks()))
    numNetworks = len(networks)

    print('\tcreate_network: networks found {}'.format(numNetworks))
    if numNetworks == 1:
      return networks[0]
    elif numNetworks == 0:
      return client.create_network({'network': {'name': name, 'admin_state_up': True, 'router:external': is_external}})
    else:
      return None
      
  except Exception as ex:
      print("an error occured getting the network, {}, {}, {}, {}, {}", ex, domain, project, name, is_external)


def select_ip(cidr):
  ar = cidr.split('/')
  ip = ipr[0]
  rg = ipr[1]

  c = ip.split('.')
  if (rg == '24'): #subnet range /24 means the last value 0 can be replaced with any value within 0-255
    return c[0] + "." + c[1] + "." + c[2] + "." + random.randint(0,256)
  else:
    return c[0] + "." + c[1] + "." + c[2] + "." + "?"
    

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