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

# Initialize LLM with optimized settings
model = OllamaLLM(
    model="llama3.1:latest",
    temperature=0,
    num_ctx=2048,  # Reduce context window
    num_thread=4   # Optimize threading
)

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

# Define state management functions
def should_end(state: AgentState) -> Union[str, None]:
    """Determine if we should end the chain"""
    messages = state['messages']
    last_message = messages[-1]
    
    if isinstance(last_message, AIMessage):
        content = last_message.content
        if "CODE_SOLUTION:" in content or "Error:" in content:
            return END
    return None

def determine_next_step(state: AgentState) -> str:
    """Route to the appropriate tool based on classification"""
    messages = state['messages']
    last_message = messages[-1]
    
    print(f"\nDetermining next step based on: {last_message.content[:100]}")
    
    if isinstance(last_message, AIMessage):
        content = last_message.content
        if "CODE_SOLUTION:" in content:
            print("Code solution found - ending workflow")
            return END
        if "TASK: Coding" in content:
            print("Routing to coding tool")
            return "coding_tool"
        if "Error:" in content:
            print("Error encountered - ending workflow")
            return END
    return "classify_tool"

# Modify call_llm function to add timeout and feedback
def call_llm(state: AgentState) -> AgentState:
    """Process messages through the LLM"""
    print("\nProcessing through LLM...")
    messages = state['messages']
    
    # Check if we need to classify
    if not any("TASK:" in msg.content for msg in messages if isinstance(msg, AIMessage)):
        system_prompt = """Classify the user's request. 
        If it's about coding, respond with exactly: TASK: Coding
        Otherwise respond with exactly: TASK: Other"""
        
        try:
            response = model.invoke(
                messages + [SystemMessage(content=system_prompt)],
                config={"timeout": 30}
            )
            return {"messages": messages + [AIMessage(content=str(response).strip())]}
        except Exception as e:
            return {"messages": messages + [AIMessage(content=f"Error: {str(e)}")]}
    
    # If we've already received a code solution, return current state
    if any("CODE_SOLUTION:" in msg.content for msg in messages if isinstance(msg, AIMessage)):
        return state
        
    return state

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

# Simplified edge configuration
workflow.add_edge(START, "llm")

workflow.add_conditional_edges(
    "llm",
    determine_next_step,
    {
        "classify_tool": "classify_tool",
        "coding_tool": "coding_tool",
        END: END
    }
)

workflow.add_edge("classify_tool", "llm")
workflow.add_edge("coding_tool", "llm")

# Compile graph
chain = workflow.compile()

# Main execution loop
while True:
    user_input = input("\nEnter your prompt (or 'exit' to quit): ")
    if user_input.lower() == "exit":
        break

    print("\nInitializing chain...")
    initial_state = {
        "messages": [
            SystemMessage(content="You are a helpful AI assistant. Be concise and direct."),
            HumanMessage(content=user_input)
        ]
    }

    try:
        print("Executing workflow...")
        result = chain.invoke(initial_state)
        
        print("\nResults:")
        for message in result["messages"]:
            if isinstance(message, AIMessage):
                print(f"Assistant: {message.content}")
    except Exception as e:
        print(f"\nWorkflow Error: {str(e)}")

print("\nExiting program...")
