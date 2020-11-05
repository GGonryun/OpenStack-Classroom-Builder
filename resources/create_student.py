import users_utility

def create_student(ledger, student):
  project = ledger[PROJECT].name
  username = student[USERNAME]
  password = users_utility.generate_user_password(username)
  users_utility.create_single_user(username, password, project, 'student')