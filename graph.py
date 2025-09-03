from typing import Dict, TypedDict,List
from langgraph.graph import StateGraph, START, END 
from langchain_core import HumanMessage


class AgentState(TypedDict):
    value: List[int]
    name: str
    result: str

def process_state(state:AgentState)-> AgentState:
    '''Handle multiple inputs'''
    state['result'] = f'Hi there {state['name'] } your sum is {sum(state["value"])}'

    return state


graph = StateGraph(AgentState)
graph.add_node('nice',process_state)
graph.set_entry_point('nice')
graph.set_finish_point("nice")

app = graph.compile()

result = app.invoke({'name': 'Shirin'})
print(result['name'])