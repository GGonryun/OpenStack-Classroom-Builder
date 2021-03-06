import argparse
import sys
import pprint
import users_utility

def create_domain(domain_id):
    print('create_domain(domain_id): {}'.format(domain_id))
    
    client = users_utility.create_keystone_client()
    domains = client.domains.list(name=domain_id)
    numDomains = len(domains)

    print('create_domain() => numDomains: {}'.format(numDomains))
    if(numDomains == 0):
        return client.domains.create(domain_id, enabled=true)
    elif(numDomains == 1):
        return domains[0]
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="The identifier/name for the domain to be created.")
    args = parser.parse_args()

    if args.id:
        print(create_domain(args.id))
    else:
        raise Exception('create_domain.py usage: --id <domain_id>')