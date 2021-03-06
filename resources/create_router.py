import argparse
import sys
import users_utility


def create_router(domain, project, name, external_network_id, external_subnet_id, external_ip_address, internal_subnet_id):
  '''
  ip_address = the ip address to attach the router to.
  subnet_id = when connecting to external services use `939dfc59-9c31-42fe-8cfa-78d2838b5b76` which is currently the external provider network's subnet id.
  '''
  print('create_router(domain: {}, project: {}, name: {}, external_network_id: {}, subnet_id: {}, external_subnet_id: {}):'.format(domain, project, external_network_id, external_subnet_id, external_ip_address, internal_subnet_id))
  try:
    api = users_utility.create_neutron_client(domain, project)

    router = find_router(api, name)
    does_router_exist = router is not None
    print('create_router(name: {}) => does router exist ? {}'.format(name, does_router_exist))
    if not router:
      external_fixed_ips = [{'ip_address': external_ip_address, 'subnet_id': external_subnet_id}]
      external_gateway_info = { 'network_id': external_network_id, 'enable_snat': True, 'external_fixed_ips': external_fixed_ips}
      router = api.create_router({'router': {'name': name, 'admin_state_up': True, 'external_gateway_info': external_gateway_info}})['router']

    link_to_router(api, router['id'], internal_subnet_id)

    print('create_router(name: {}): finished creating router'.format(name))
    return router
  except Exception as ex:
    print("create_router: an error has occured", ex, domain, project, name, external_network_id,  external_subnet_id, external_ip_address, internal_subnet_id)
    return None

def find_router(api, name):
  '''
  name can also be an id.
  '''
  print('find_router(api, name: {})'.format(name))
  routers = list(filter(lambda s : s['name'] == name or s['id'] == name, api.list_routers()['routers']))
  numRouters = len(routers)
  does_router_exist = numRouters == 1
  print('find_router(name: {}) => does router exist ? {}'.format(name, does_router_exist))
  if does_router_exist:
    return routers[0]
  
  return None

def link_to_router(api, router_id, subnet_id):
  print('link_to_router(api: <HIDDEN>, router_id: {}, subnet_id: {})', router_id, subnet_id)
  try:
    if subnet_id:
      api.add_interface_router(router_id, {'subnet_id': subnet_id})
      print('link_to_router(router_id: {}, subnet_id: {}) => created link'.format(router_id, subnet_id))
  except:
    print('link_to_router() => link already exists')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--domain", help="name of domain for the router")
  parser.add_argument("--project", help="name of project for the router")
  parser.add_argument("--name", help="name for the router")
  parser.add_argument("--internal-sid", help="the internal subnet id to connect to")
  parser.add_argument("--external-nid", help="the external network id that will provide outside connectivity; it should be a guid such as: '939dfc59-9c31-42fe-8cfa-78d2838b5b76'")
  parser.add_argument("--external-sid", help="the external subnet id that will provide outside connectivity.")
  parser.add_argument("--ip", help="an ip address on the external-sid.")
  args = parser.parse_args()

  if args.domain and args.project and args.name and args.external_nid and args.external_sid and args.internal_sid :
      print(create_router(args.domain, args.project, args.name, args.external_nid, args.external_sid, args.ip, args.internal_sid))
  elif args.domain and args.project and args.name and args.external_nid and args.external_sid and args.ip:
      print(create_router(args.domain, args.project, args.name, None, args.external_nid, args.external_sid, args.ip))
  else:
      raise Exception('create_router.py incorrect usage')