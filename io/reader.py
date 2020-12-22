from functools import partial
import pandas
import pprint
import sys
import yaml
import copy

##### USER DEFINED CONSTANT #####
EMPTY_STRING = ""
FILE_ACCESS = "r"
MACHINES_KEY = "Machines"
STUDENTS_KEY = "Students"
PER_PROJECT_KEY = "PerProject"
PER_USER_KEY = "PerUser"

# global variable for all functions to push errors, in the end this property is returned to the caller using "read_yaml".
errors = []

##### Imperative Shell
def read_yaml(path):
  print("read_yaml(path: {})".format(path))
  content = open(path, FILE_ACCESS)
  data = yaml.load(content, Loader=yaml.SafeLoader)
  classroom = clean_up(data)
  print("read_yaml(): converted data from yaml to dict {}".format(classroom))
  return [classroom, errors]

##### Functional Core
# todo: unit test
def clean_up(data):
  filterNonEmpty = partial(filter, lambda obj: obj != None)

  if(STUDENTS_KEY not in data or MACHINES_KEY not in data):
    print("clean_up() => no students or machines specified, skipping clean up")
    return data

  clone = copy.deepcopy(data)
  if(STUDENTS_KEY in clone):
    print("clean_up() => cleaning up students")
    clone[STUDENTS_KEY] = list(filterNonEmpty(map(student_csv_to_dict, clone[STUDENTS_KEY])))
    
  if(MACHINES_KEY in clone):
    print("clean_up() => cleaning up machines")
    if PER_PROJECT_KEY in clone[MACHINES_KEY]:
      print("clean_up() => creating project machines")
      clone[MACHINES_KEY][PER_PROJECT_KEY] = list(filterNonEmpty(map(machine_csv_to_dict, clone[MACHINES_KEY][PER_PROJECT_KEY])))
    if PER_USER_KEY in clone[MACHINES_KEY]:
      print("clean_up() => creating user machines")
      clone[MACHINES_KEY][PER_USER_KEY] = list(filterNonEmpty(map(machine_csv_to_dict, clone[MACHINES_KEY][PER_USER_KEY])))

  return clone

def student_csv_to_dict(csv):
  print("student_csv_to_dict(csv: {csv})".format(csv))
  arr = csv.split(',')
  access = partial(safeAccess, arr)

  if(len(arr) == 3):
    student = {"FirstName": access(0), "LastName": access(1), "Username": access(2)}
    print("student_csv_to_dict() => student {}".format(student))
    return student
  else:
    errors.append("failed to process student {}".format(csv))
    return None

def machine_csv_to_dict(csv):
  print("tmachine_csv_to_dict({})".format(csv))
  arr = csv.split(',')
  access = partial(safeAccess, arr)
  if(len(arr) >= 5):
    machine = { "Name": access(0), "Instances": access(1), "Image": access(2), "Flavor": access(3), "Network": access(4), "Password": access(5) }
    print("machine_csv_to_dict() => created machine {}".format(machine))
    return machine
  else:
    errors.append("failed to process machine {}".format(csv))
    return None

def safeAccess(array, index):
  if(index >= len(array) or index < 0):
    return None
  return array[index]

if __name__ == '__main__': # Program entrance
    file_path = sys.argv[1]
    print ('Testing Reader.py {}'.format(file_path))
    read_yaml(file_path)