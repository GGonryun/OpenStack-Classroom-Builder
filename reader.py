import pandas
import pprint
import sys
import yaml
import copy

##### USER DEFINED CONSTANT #####
EMPTY_STRING = ""
READ_ONLY_ACCESS = "r"


# global variable for all functions to push errors, in the end this property is returned to the caller using "read_yaml".
errors = []

def read_yaml(path):
  try:
    print("\treader: read_yaml: try: reading contents from {}".format(path))
    content = read_file(path)
    data = yaml.load(content, Loader=yaml.SafeLoader)
    classroom = clean_up_roster(data)
    print("\treader: read_yaml: try: converted data from yaml to dict {}".format(classroom))
    return [classroom, errors]
  except Exception as e:
    print("\treader: read_yaml: except: an error has occured reading yaml {}".format(e))

def clean_up_roster(data):
  # Validation
  print("\treader: clean_up_roster: cleaning up {}".format(data))
  if(data['Users'] == None or data['Users']['Roster'] == None):
    raise ValueError("A class roster must be specified!")

  # Clone object
  print("\treader: clean_up_roster: cloning original dict")
  clone = copy.deepcopy(data)

  # Clean up roster
  roster = []
  for csv in clone['Users']['Roster']:
    student = csv_to_dict(csv)
    if(student != None):
      roster.append(student)
  
  # Return clone
  print("\treader: clean_up_roster: updated roster {}".format(roster))
  clone['Users']['Roster'] = roster
  return clone

def csv_to_dict(csv):
  print("\treader: separate_csv: converting csv into dictionary {}".format(csv))
  arr = csv.split(',')
  student = None
  if(len(arr) == 3):
    student = {"FirstName": arr[0], "LastName": arr[1], "UserName": arr[2]}
    print("\treader: separate_csv: created student {}".format(student))
  else:
    errors.append("failed to process student {}".format(csv))
  return student

# Opens a file and returns its contents, if a file is not found the function returns an empty string.
def read_file(path):
  try:
    print("\treader: read_file: try: opening file at {}".format(path))
    content = open(path, "r")
    print("\treader: read_file: try: content received {}".format(content))
    return content
  except Exception as e:
    print("\treader: read_file: except: an error has occured opening files {}, {}".format(path, e))
    return EMPTY_STRING 

if __name__ == '__main__': # Program entrance
    file_path = sys.argv[1]
    print ('Testing Reader.py {}'.format(file_path))
    read_yaml(file_path)
