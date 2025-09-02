"""
Simplified LangGraph Demo with Ollama Llama-3.1
A streamlined example that's responsive and easy to understand.
"""

from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List, Annotated
import operator

# Initialize Ollama LLM
llm = OllamaLLM(model="llama3.1:latest")


# Define the conversation state
class ChatState(TypedDict):
    messages: Annotated[List, operator.add]
    user_input: str


def chat_node(state: ChatState):
    """
    Process user input and generate response
    """
    user_input = state["user_input"]

    # Create a simple prompt
    prompt = f"User: {user_input}\nAssistant:"

    # Get response from Ollama (with shorter max tokens for faster response)
    response = llm.invoke(prompt)

    # Add messages to conversation history
    new_messages = [HumanMessage(content=user_input), AIMessage(content=response)]

    return {"messages": new_messages}


def should_continue(state: ChatState):
    """Check if conversation should continue"""
    user_input = state["user_input"].lower().strip()
    if user_input in ["quit", "exit", "bye", "goodbye", "stop"]:
        return "end"
    return "continue"


def create_chat_graph():
    """Create the LangGraph workflow"""
    workflow = StateGraph(ChatState)

    # Add the chat node
    workflow.add_node("chat", chat_node)

    # Set entry point
    workflow.set_entry_point("chat")

    # Add conditional edges
    workflow.add_conditional_edges(
        "chat", should_continue, {"continue": "chat", "end": END}
    )

    # Add memory for conversation persistence
    memory = MemorySaver()

    # Compile the graph
    return workflow.compile(checkpointer=memory)


def run_chat():
    """Run the interactive chat"""
    print("🤖 LangGraph + Ollama Demo")
    print("=" * 30)
    print("Type 'quit' to exit")
    print("=" * 30)

    app = create_chat_graph()

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "bye", "goodbye", "stop"]:
                print("\n🤖 Goodbye! 👋")
                break

            print("🤖 Assistant: ", end="", flush=True)

            # Run the graph with current input
            current_state = ChatState(user_input=user_input, messages=[])
            for state in app.stream(current_state):
                if "chat" in state and "messages" in state["chat"]:
                    messages = state["chat"]["messages"]
                    if messages:
                        # Get the AI response (last message)
                        ai_response = messages[-1].content
                        print(ai_response)

        except KeyboardInterrupt:
            print("\n\n🤖 Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    print("🔄 Starting LangGraph demo...")
    run_chat()
