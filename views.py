from todo.models import users,todos
session={}

def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user=[user for user in users if user["username"] == username and user["password"] == password]
    return user


class SignInView:
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            session["user"]=user[0]
            print("success")
        else:
            print("invalid")

class TodosView():
    def get(self,*args,**kwargs):
        return todos
    def post(self,*args,**kwargs):
        print(kwargs)
        userId=session["user"]["id"]
        kwargs["userId"]=userId
        print(kwargs)
        todos.append(kwargs)
        print("todo added")
        print(todos)

class MyTodoListView:
    def get(self,*args,**kwargs):
        print(session)
        userId=session["user"]["id"]
        print(userId)
        my_todos=[todo for todo in todos if todo["userId"]==userId]
        return my_todos

class TodosDetailsView:

    def get_object(self,id):
        todo=[todo for todo in todos if todo["todoId"]==id]
        return todo
    def get(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        todo=self.get_object(todo_id)
        return todo

    def delete(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        data=self.get_object(todo_id)
        if data:
            todo=data[0]
            todos.remove(todo)
            print("todo removed")
            print(len(todos))
    def put(self,*args,**kwargs):
        print(kwargs)
        todo_id=kwargs.get("todo_id")
        instance=self.get_object(todo_id)
        data=kwargs.get("data")
        if instance:
            post_obj=instance[0]
            post_obj.update(data)
            return post_obj

def signout(*args,**kwargs):
    user=session.pop("user")
    print(f"the user {user['username']}  has been logged out")




log=SignInView()
log.post(username="anu",password="Password@123")
mytodos=MyTodoListView()
print(mytodos.get())

todo_detail=TodosDetailsView()
todo_detail.delete(todo_id=6)
print(todo_detail.get(todo_id=3))

data={
    "task_name":"new gbill"
}
print(todo_detail.put(todo_id=4,data=data))
#print(session)
#data=TodosView()
#print(data.get())
#data.post(todoId=9,
#          task_name="ebill",
#          completed="False")

signout()