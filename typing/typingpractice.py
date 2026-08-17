from typing import TypedDict, Optional, Annotated, Literal
import operator

name:str = input()
age:int = int(input())
messages : list[str] = ["Hii", "Hello", "How are you??", "what are you??"]
address : Optional[str] = None
classname : Literal["12th", "11th"]

class State(TypedDict):
    name:str
    age:int | str
    messages: Annotated[list[str], operator.add]

def data(state: State)->Optional[State]:
    
    print(f"My Name is {state['name']} and I am {state['age']} years old..\nMessage:{state["messages"]}")
    state = {"name":"Ram", "age":44, "messages": [messages[1]]}
    
    return state


result = data({
    "name": "Raju Yadav", "age": 22,"messages":[messages[0]]
})
print(result)

