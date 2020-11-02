
# INSTRUCTIONS:
# This script should be run before a user has logged on to change their password.
# This script assumes you have loaded in the required variables to log into the CLI.
# This script assumes the csv file is located in the same directory.
# The CSV file must have non-nullable columns: Username, Project.
# The CSV file may have nullable columns: Password (If included, the specified password is used instead).

# use: python create_vms image_id metasploitable flavor_id network_id users.csv
#      derive value for flavor_id from: openstack flavor list
#      derive value for network_id from: openstack network list
#      derive value for image_id from: openstack image list


# Nova clients are created to be project specific, the project id identifies which nova client to use.
# If a nova client does not exist, a process-long client must be opened and stored in this list.
PER_PROJECT_KEY = "PerProject"
PER_USER_KEY = "PerUser"



def create_vm(client, name, instances, image_id, flavor_id, network_id):
    try:
        return client.servers.create(name=name, image=image_id, flavor=flavor_id, nics=[{ 'net-id': network_id }])
    except:
        pprint.pprint("an error has occured creating {}, {}, {}, {}, {}".format(username, vm_name, IMAGE_ID, FLAVOR_ID, NETWORK_ID))
        return None
