import users_utility

PROJECT = 'Project'
USERNAME = 'Username'
STUDENT = 'student'

def create_student(ledger, student):
  project = ledger[PROJECT].name
  username = student[USERNAME]
  password = users_utility.generate_user_password(username)
  users_utility.create_single_user(username, password, project, STUDENT)