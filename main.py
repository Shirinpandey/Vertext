from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from typing import Sequence, TypedDict, Dict, Union
from tools.classify_tool import classify
from tools.coding_tool import coding
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolNode
from typing import Annotated
from langchain.tools import Tool

# Initialize LLM
model = OllamaLLM(model="llama3.1:latest", temperature=0)

# Define tools
tools = [
    Tool(
        name="classify",
        description="Classifies text into Coding, Writing, Research, or Summarization",
        func=classify
    ),
    Tool(
        name="coding",
        description="Handles coding-related tasks",
        func=coding
    )
]

# Define state type
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_step: str

# Define state management functions
def should_end(state: AgentState) -> Union[str, None]:
    """Determine if we should end the chain"""
    messages = state['messages']
    last_message = messages[-1]
    if isinstance(last_message, AIMessage):
        if "FINAL ANSWER:" in last_message.content:
            return END
    return None

def determine_next_step(state: AgentState) -> str:
    """Route to the appropriate tool based on classification"""
    messages = state['messages']
    last_message = messages[-1]
    if isinstance(last_message, AIMessage):
        if "Coding" in last_message.content:
            return "coding_tool"
    return "classify_tool"

def call_llm(state: AgentState) -> AgentState:
    """Process messages through the LLM"""
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": messages + [AIMessage(content=response)]}

# Create graph
workflow = StateGraph(AgentState)

# Add nodes
classify_node = ToolNode(
    tools=[tools[0]],
    name="classify_tool"
)

coding_node = ToolNode(
    tools=[tools[1]],
    name="coding_tool"
)

# Add nodes to graph
workflow.add_node("classify_tool", classify_node)
workflow.add_node("coding_tool", coding_node)
workflow.add_node("llm", call_llm)

# Add edges
workflow.add_edge(START, "llm")
workflow.add_edge("llm", determine_next_step)
workflow.add_edge("classify_tool", "llm")
workflow.add_edge("coding_tool", "llm")
workflow.add_conditional_edges(
    "llm",
    should_end,
    {
        None: determine_next_step,
        END: END,
    }
)

# Compile graph
chain = workflow.compile()

# Main execution loop
while True:
    user_input = input("Enter your prompt (or 'exit' to quit): ")
    if user_input.lower() == "exit":
        break

    # Initialize state
    initial_state = {
        "messages": [
            SystemMessage(content="You are a helpful AI assistant that can classify and handle coding tasks."),
            HumanMessage(content=user_input)
        ],
        "next_step": "classify_tool"
    }

    try:
        # Execute the chain
        result = chain.invoke(initial_state)
        
        # Print responses
        for message in result["messages"]:
            if isinstance(message, AIMessage):
                print(f"\nAssistant: {message.content}")
    except Exception as e:
        print(f"Error: {str(e)}")
