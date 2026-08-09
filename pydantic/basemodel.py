from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum

# ----------BASE MODEL AND FIELD------------------
class User(BaseModel):
    username: str = Field(min_length= 3, max_length=16) 
    name: str
    age: int | None = Field(ge= 18, le= 65)
    price: float
    quantity: int 

user = User(username= "ruuh123",name="Ruuh",age= 22, price= 7000.45, quantity= 5)
'''print(type(user))
print(type(user.age))
print(user.username)
print(user)
print(user.age)
print(user.name)
print(user.price)
print(user.quantity)'''
# print(user.model_dump)
# print(user.model_dump_json)

# ---------------With value and Literal----------------
class userModel(BaseModel):
    
    username: str = Field(min_length= 5 , max_length= 16)
    password: str = Field(min_length=5, max_length= 16)
    role: Literal["admin", "user", "manager"]

# --------------Enum----------------
class Role(str, Enum):
    
    ADMIN = "admin"
    USER : userModel

class USER(BaseModel):
    
    name: str
    role : userModel
    
user1 = USER(name= "rajuyadav", role= {"username": "rajuyadav", "password":"12345", "role":"manager"})


# ------------------Custom Validator------------
# 1. field_validator
from pydantic import field_validator

class School(BaseModel):
    name: str
    classname: str
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        
        if len(value) > 30:
           raise ValueError("School name must be 16 characters or less")
        return value.lower()

school1 = School(name = "ALFANSO INTERNATIONAL SCHOOL", classname= "12th")    
# print(school1)

#2.model_validator------------------
from pydantic import model_validator

class Student(BaseModel):
    
    name: str
    age: int
    classname:str
    
    @model_validator(mode="after")
    def validate_student(self):
        
        if self.classname == "12th" and self.age < 18:
            raise ValueError("12th class student must be at least 18 years old.")
        return self
    
# student1 = Student(name="Rohan", age= "19", classname="12th")
# print(student1.model_dump(include={"name", "age"}))  
# print(student1.model_dump(exclude={"name", "age"}))   
# print(type(student1.model_dump_json(include={"name", "age"})))    
 

# --------------strict mdoe for validation------------
from pydantic import ConfigDict

class User1(BaseModel):
    model_config = ConfigDict(strict= True)
    name :str
    age: int
    username : int = Field(strict= True)
    
user1 = User1(name="rama", age= 19, username= 21)
# print(user1)    

# ------------computed field--------
from pydantic import computed_field

class Product(BaseModel):
    
    price: float
    quantity: int 
    
    @computed_field
    @property
    def total(self) -> float:
        
        return self.price * self.quantity

product1 = Product(price= 1990.12, quantity= 5)
# print(f"\nprice: {product1.price} * quantity: {product1.quantity} = {product1.total:.2f}")    