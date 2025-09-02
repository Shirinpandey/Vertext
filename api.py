from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List, Annotated
import operator

# Initialize Ollama LLM
llm = OllamaLLM(model="llama3.1:latest")


# Define the state structure for our graph
class GraphState(TypedDict):
    messages: Annotated[List, operator.add]
    user_input: str


# Create a prompt template for the conversation
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant. Be conversational and helpful. Keep your responses concise but informative.",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{user_input}"),
    ]
)


def chatbot_node(state: GraphState):
    """
    Main chatbot node that processes the conversation
    """
    messages = state.get("messages", [])
    user_input = state["user_input"]

    # Create the prompt with message history
    formatted_prompt = prompt.format_messages(messages=messages, user_input=user_input)

    # Get response from Ollama
    response = llm.invoke(formatted_prompt)

    # Add messages to the conversation history
    new_messages = [HumanMessage(content=user_input), AIMessage(content=response)]

    return {"messages": new_messages, "user_input": user_input}


def should_continue(state: GraphState):
    """
    Determine if we should continue the conversation
    """
    user_input = state["user_input"].lower().strip()
    if user_input in ["quit", "exit", "bye", "goodbye"]:
        return "end"
    return "continue"


# Build the graph
def create_conversation_graph():
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("chatbot", chatbot_node)

    # Set entry point
    workflow.set_entry_point("chatbot")

    # Add conditional edges
    workflow.add_conditional_edges(
        "chatbot", should_continue, {"continue": "chatbot", "end": END}
    )

    # Add memory to persist conversation state
    memory = MemorySaver()

    # Compile the graph
    app = workflow.compile(checkpointer=memory)

    return app


# Demo function to run the conversational agent
def run_demo():
    """
    Run a demonstration of the LangGraph conversational agent
    """
    print("🤖 LangGraph + Ollama Llama-3.1 Demo")
    print("=" * 40)
    print("Type 'quit', 'exit', 'bye', or 'goodbye' to end the conversation.")
    print("=" * 40)

    app = create_conversation_graph()

    # Thread configuration for memory persistence
    config = RunnableConfig(configurable={"thread_id": "demo_conversation"})

    # Initial state
    initial_state = GraphState(messages=[], user_input="")

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            # Check for exit conditions
            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                print("\n🤖 Assistant: Goodbye! Have a great day!")
                break

            # Update state with user input
            current_state = GraphState(messages=[], user_input=user_input)

            # Run the graph
            print("\n🤖 Assistant: ", end="", flush=True)

            final_state = None
            for state in app.stream(current_state, config):
                final_state = state

            # Get the latest AI message
            if final_state and "chatbot" in final_state:
                messages = final_state["chatbot"]["messages"]
                if messages:
                    ai_message = messages[-1]  # Get the last AI message
                    if hasattr(ai_message, "content"):
                        print(ai_message.content)
                    else:
                        print(ai_message)

        except KeyboardInterrupt:
            print("\n\n🤖 Assistant: Goodbye! Have a great day!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")


# Simple function to test the LLM connection
def test_ollama_connection():
    """
    Test if Ollama is running and the model is available
    """
    try:
        response = llm.invoke("Hello! Can you confirm you're working?")
        print("✅ Ollama connection successful!")
        print(f"🤖 Response: {response}")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("Make sure Ollama is running and llama3.1:8b model is available.")
        return False


if __name__ == "__main__":
    print("Testing Ollama connection...")
    if test_ollama_connection():
        print("\nStarting LangGraph demo...")
        run_demo()
    else:
        print("\nPlease ensure Ollama is running with: ollama serve")
        print("And the model is available with: ollama pull llama3.1:8b")
