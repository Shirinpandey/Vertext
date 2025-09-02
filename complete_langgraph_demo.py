"""
Complete LangGraph + Ollama Example
This demonstrates a working conversational agent with state management,
memory, and conditional flow control using LangGraph.
"""

from langchain_ollama import OllamaLLM
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
import sys

# Initialize the LLM
llm = OllamaLLM(model="llama3.1:latest")


class ConversationState(TypedDict):
    """State object that gets passed between nodes"""

    user_input: str
    ai_response: str
    conversation_history: str
    turn_count: int


def process_input_node(state: ConversationState) -> ConversationState:
    """
    Main processing node that generates AI responses
    """
    user_input = state["user_input"]
    history = state.get("conversation_history", "")
    turn_count = state.get("turn_count", 0)

    # Build context-aware prompt
    if history:
        prompt = f"Previous conversation:\n{history}\n\nUser: {user_input}\nAssistant:"
    else:
        prompt = f"User: {user_input}\nAssistant:"

    # Generate response
    ai_response = llm.invoke(prompt)

    # Update conversation history
    new_history = f"{history}\nUser: {user_input}\nAssistant: {ai_response}"

    return {
        "user_input": user_input,
        "ai_response": ai_response,
        "conversation_history": new_history,
        "turn_count": turn_count + 1,
    }


def decide_next_step(state: ConversationState) -> Literal["continue", "end"]:
    """
    Conditional edge function that decides whether to continue or end
    """
    user_input = state["user_input"].lower().strip()

    # End conditions
    if user_input in ["quit", "exit", "bye", "goodbye", "stop", "end"]:
        return "end"

    # Continue the conversation
    return "continue"


def create_conversation_graph():
    """
    Create and return the compiled LangGraph workflow
    """
    # Initialize the graph
    workflow = StateGraph(ConversationState)

    # Add the processing node
    workflow.add_node("process", process_input_node)

    # Set the entry point
    workflow.set_entry_point("process")

    # Add conditional edges
    workflow.add_conditional_edges(
        "process",
        decide_next_step,
        {
            "continue": "process",  # Loop back to process more input
            "end": END,  # End the conversation
        },
    )

    # Compile the graph
    return workflow.compile()


def run_demo():
    """
    Run the interactive demonstration
    """
    print("🚀 LangGraph + Ollama Llama-3.1 Demonstration")
    print("=" * 50)
    print("This demo shows:")
    print("• 🔄 State management across conversation turns")
    print("• 💭 Context-aware responses using conversation history")
    print("• 🎯 Conditional flow control (continue/end decisions)")
    print("• 🧠 Memory persistence within the graph")
    print("=" * 50)
    print("Commands: 'quit', 'exit', 'bye', 'goodbye', 'stop', 'end' to exit")
    print("=" * 50)

    # Create the graph
    app = create_conversation_graph()

    # Initialize state
    current_state = ConversationState(
        user_input="", ai_response="", conversation_history="", turn_count=0
    )

    try:
        while True:
            # Get user input
            user_input = input(
                f"\n👤 You (Turn {current_state.get('turn_count', 0) + 1}): "
            ).strip()

            if not user_input:
                continue

            # Update state with new input
            current_state["user_input"] = user_input

            # Check for immediate exit
            if user_input.lower() in ["quit", "exit", "bye", "goodbye", "stop", "end"]:
                print(
                    "\n🤖 Assistant: Goodbye! Thanks for trying the LangGraph demo! 👋"
                )
                break

            print("\n🤖 Assistant: ", end="", flush=True)

            # Stream through the graph
            final_state = None
            for step in app.stream(current_state):
                final_state = step

            # Extract and display the response
            if final_state and "process" in final_state:
                response_state = final_state["process"]
                ai_response = response_state["ai_response"]
                print(ai_response)

                # Update current state for next iteration
                current_state = response_state

    except KeyboardInterrupt:
        print("\n\n🤖 Assistant: Goodbye! Thanks for trying the demo! 👋")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Please make sure Ollama is running with the llama3.1:latest model.")


def test_setup():
    """
    Test if everything is set up correctly
    """
    try:
        print("🔧 Testing Ollama connection...")
        test_response = llm.invoke("Say 'Hello' if you can hear me.")
        print(f"✅ Ollama is working! Response: {test_response}")
        return True
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Check if model exists: ollama list")
        print("3. Pull model if needed: ollama pull llama3.1")
        return False


if __name__ == "__main__":
    print("🔍 Checking setup...")
    if test_setup():
        print("\n" + "=" * 50)
        run_demo()
    else:
        print("\n❌ Setup failed. Please fix the issues above and try again.")
        sys.exit(1)
