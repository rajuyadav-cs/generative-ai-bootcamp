from pydantic import BaseModel

class User(BaseModel):
    
    name: str
    age: int

user = User(name="Ruuh", age= "21")
print(type(user))
print(type(user.age))
print(user)
print(user.age)
print(user.name)
    