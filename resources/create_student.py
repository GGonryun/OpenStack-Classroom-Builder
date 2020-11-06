import users_utility
import create_student_users

PROJECT = 'Project'
USERNAME = 'Username'
STUDENT = 'Student'
PASSWORD = 'Password'

def create_student(ledger, student):
  print('create_student(ledger, student):', ledger, student)
  project = ledger[PROJECT].name
  username = student[USERNAME]
  
  student[PROJECT] = project
  student[PASSWORD] = users_utility.generate_user_password(username)

  create_student_users.create_student_users([student])