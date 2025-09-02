from typing import Dict, TypedDict
from langgraph.graph import StateGraph 

class AgentState(TypedDict):
    name: str

def compliment_agent(state:AgentState)-> AgentState:
    state['name'] = f'{state['name'] } youre doing so well'
    return state


graph = StateGraph(AgentState)
graph.add_node('nice',compliment_agent)
graph.set_entry_point('nice')
graph.set_finish_point("nice")

app = graph.compile()

result = app.invoke({'name': 'Shirin'})
print(result['name'])