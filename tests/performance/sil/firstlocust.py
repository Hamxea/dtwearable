from locust import TaskSet, User


def login(l):
    print("Login")
    
def logout(m):
    print("Logout")
    

class UserBehaviour(TaskSet):
    tasks = [login, logout]

class User(User):
    task_set = UserBehaviour

