from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage,AIMessage, SystemMessage, BaseMessage,ToolMessage
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, START, END 
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

class AgentState(TypedDict):
    message: str

model = OllamaLLM(model="llama3.1:latest")

def process_state(state:AgentState)-> AgentState:
    '''It will handle the request you send'''
    # sends in the initial state of messages to the model 
    response = model.invoke(state['message'])
    # appends the state with the response from the model
    state['message'].append(AIMessage(content = response.content))
    print(response.content)

    return state

graph = StateGraph(AgentState)
graph.add_node('process',process_state)
graph.add_edge(START,'process')
graph.add_edge("process",END)   
agent = graph.compile()

conversion_history = []
user_input = input("Enter your prompt: ")
# this is where you call the agent
while user_input.lower() != "exit":
    # you append the user input to state and pass it as message 
    conversion_history.append(HumanMessage(content = user_input))
    result = agent.invoke({'message': [HumanMessage(content=conversion_history)]})
    # overwrite the variable with the new state and pass that again to be appended
    conversion_history = result['message']
    user_input = input("Enter your prompt: ")