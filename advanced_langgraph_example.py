"""
Advanced LangGraph Example with Ollama Llama-3.1
This example demonstrates more complex graph structures with multiple nodes,
conditional routing, and tool usage.
"""

from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List, Annotated, Literal
import operator
import re
import random

# Initialize Ollama LLM
llm = OllamaLLM(model="llama3.1:latest")


# Define the state structure
class AdvancedGraphState(TypedDict):
    messages: Annotated[List, operator.add]
    user_input: str
    current_task: str
    analysis_result: str
    needs_clarification: bool


# Define different prompts for different tasks
CLASSIFIER_PROMPT = """
Analyze the user's input and classify it into one of these categories:
1. "question" - User is asking a question that needs a direct answer
2. "task" - User wants help with a specific task or problem
3. "creative" - User wants creative content (story, poem, idea, etc.)
4. "analysis" - User wants analysis of data, text, or a concept
5. "clarification" - The request is unclear and needs clarification

User input: {user_input}

Respond with only the category name (question, task, creative, analysis, or clarification).
"""

ANSWER_PROMPT = """
You are a helpful AI assistant. Provide a clear, informative answer to the user's question.
Keep your response concise but complete.

User question: {user_input}
"""

TASK_HELPER_PROMPT = """
You are a task-oriented AI assistant. Help the user accomplish their specific task.
Provide step-by-step guidance or practical solutions.

User task: {user_input}
"""

CREATIVE_PROMPT = """
You are a creative AI assistant. Help the user with their creative request.
Be imaginative, engaging, and original in your response.

Creative request: {user_input}
"""

ANALYSIS_PROMPT = """
You are an analytical AI assistant. Provide thoughtful analysis based on the user's request.
Break down complex topics and provide insights.

Analysis request: {user_input}
"""

CLARIFICATION_PROMPT = """
The user's request is unclear. Ask helpful questions to better understand what they need.
Be friendly and specific in your clarification questions.

Unclear request: {user_input}
"""


def classify_input_node(state: AdvancedGraphState):
    """
    Classify the user input to determine the appropriate response type
    """
    user_input = state["user_input"]

    # Use LLM to classify the input
    classification = llm.invoke(CLASSIFIER_PROMPT.format(user_input=user_input))
    classification = classification.strip().lower()

    # Map classification to task
    task_mapping = {
        "question": "answer_question",
        "task": "help_with_task",
        "creative": "generate_creative",
        "analysis": "provide_analysis",
        "clarification": "ask_clarification",
    }

    current_task = task_mapping.get(classification, "ask_clarification")

    return {
        "current_task": current_task,
        "needs_clarification": current_task == "ask_clarification",
    }


def answer_question_node(state: AdvancedGraphState):
    """
    Handle direct questions
    """
    user_input = state["user_input"]
    response = llm.invoke(ANSWER_PROMPT.format(user_input=user_input))

    new_messages = [
        HumanMessage(content=user_input),
        AIMessage(content=f"📝 Answer: {response}"),
    ]

    return {"messages": new_messages}


def help_with_task_node(state: AdvancedGraphState):
    """
    Help with specific tasks
    """
    user_input = state["user_input"]
    response = llm.invoke(TASK_HELPER_PROMPT.format(user_input=user_input))

    new_messages = [
        HumanMessage(content=user_input),
        AIMessage(content=f"🛠️ Task Help: {response}"),
    ]

    return {"messages": new_messages}


def generate_creative_node(state: AdvancedGraphState):
    """
    Generate creative content
    """
    user_input = state["user_input"]
    response = llm.invoke(CREATIVE_PROMPT.format(user_input=user_input))

    new_messages = [
        HumanMessage(content=user_input),
        AIMessage(content=f"🎨 Creative Response: {response}"),
    ]

    return {"messages": new_messages}


def provide_analysis_node(state: AdvancedGraphState):
    """
    Provide analytical responses
    """
    user_input = state["user_input"]
    response = llm.invoke(ANALYSIS_PROMPT.format(user_input=user_input))

    new_messages = [
        HumanMessage(content=user_input),
        AIMessage(content=f"📊 Analysis: {response}"),
    ]

    return {"messages": new_messages, "analysis_result": response}


def ask_clarification_node(state: AdvancedGraphState):
    """
    Ask for clarification when input is unclear
    """
    user_input = state["user_input"]
    response = llm.invoke(CLARIFICATION_PROMPT.format(user_input=user_input))

    new_messages = [
        HumanMessage(content=user_input),
        AIMessage(content=f"❓ Clarification needed: {response}"),
    ]

    return {"messages": new_messages}


def route_to_handler(
    state: AdvancedGraphState,
) -> Literal[
    "answer_question",
    "help_with_task",
    "generate_creative",
    "provide_analysis",
    "ask_clarification",
]:
    """
    Route to the appropriate handler based on classification
    """
    task = state["current_task"]
    # Ensure the task is one of the valid literal values
    valid_tasks = [
        "answer_question",
        "help_with_task",
        "generate_creative",
        "provide_analysis",
        "ask_clarification",
    ]
    if task in valid_tasks:
        return task  # type: ignore
    else:
        return "ask_clarification"


def should_continue(state: AdvancedGraphState):
    """
    Determine if conversation should continue
    """
    user_input = state["user_input"].lower().strip()
    if user_input in ["quit", "exit", "bye", "goodbye", "stop"]:
        return "end"
    return "continue"


def create_advanced_graph():
    """
    Create the advanced LangGraph workflow
    """
    workflow = StateGraph(AdvancedGraphState)

    # Add all nodes
    workflow.add_node("classify", classify_input_node)
    workflow.add_node("answer_question", answer_question_node)
    workflow.add_node("help_with_task", help_with_task_node)
    workflow.add_node("generate_creative", generate_creative_node)
    workflow.add_node("provide_analysis", provide_analysis_node)
    workflow.add_node("ask_clarification", ask_clarification_node)

    # Set entry point
    workflow.set_entry_point("classify")

    # Add conditional edges from classifier to handlers
    workflow.add_conditional_edges(
        "classify",
        route_to_handler,
        {
            "answer_question": "answer_question",
            "help_with_task": "help_with_task",
            "generate_creative": "generate_creative",
            "provide_analysis": "provide_analysis",
            "ask_clarification": "ask_clarification",
        },
    )

    # All handler nodes end the current cycle
    for node in [
        "answer_question",
        "help_with_task",
        "generate_creative",
        "provide_analysis",
        "ask_clarification",
    ]:
        workflow.add_edge(node, END)

    # Add memory
    memory = MemorySaver()

    # Compile the graph
    app = workflow.compile(checkpointer=memory)

    return app


def run_advanced_demo():
    """
    Run the advanced LangGraph demo
    """
    print("🚀 Advanced LangGraph + Ollama Demo")
    print("=" * 50)
    print("This demo classifies your input and routes to specialized handlers:")
    print("• 📝 Questions → Direct answers")
    print("• 🛠️ Tasks → Step-by-step help")
    print("• 🎨 Creative requests → Imaginative responses")
    print("• 📊 Analysis → Detailed breakdowns")
    print("• ❓ Unclear inputs → Clarification questions")
    print("=" * 50)
    print("Type 'quit', 'exit', 'bye', or 'goodbye' to end.")
    print("=" * 50)

    app = create_advanced_graph()
    config = RunnableConfig(configurable={"thread_id": "advanced_demo"})

    # Example prompts to try
    examples = [
        "What is machine learning?",
        "Help me write a Python function to sort a list",
        "Write a short poem about programming",
        "Analyze the pros and cons of remote work",
        "Something unclear and vague",
    ]

    print("💡 Try these examples:")
    for i, example in enumerate(examples, 1):
        print(f"   {i}. {example}")
    print()

    while True:
        try:
            user_input = input("👤 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "bye", "goodbye", "stop"]:
                print(
                    "\n🤖 Assistant: Thank you for trying the advanced demo! Goodbye!"
                )
                break
            # Run through the graph
            print("\n🔄 Processing...", end="", flush=True)

            current_state: AdvancedGraphState = {
                "user_input": user_input,
                "messages": [],
                "current_task": "",
                "analysis_result": "",
                "needs_clarification": False,
            }

            final_state = None
            for state in app.stream(current_state, config=config):
                final_state = state
                final_state = state

            # Extract and display the response
            if final_state:
                for node_name, node_state in final_state.items():
                    if "messages" in node_state and node_state["messages"]:
                        ai_message = node_state["messages"][-1]
                        if hasattr(ai_message, "content"):
                            print(f"\r🤖 {ai_message.content}")
                        else:
                            print(f"\r🤖 {ai_message}")
                        break

        except KeyboardInterrupt:
            print("\n\n🤖 Assistant: Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    run_advanced_demo()
