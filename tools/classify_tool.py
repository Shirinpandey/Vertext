from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage

model = OllamaLLM(model="llama3.1:latest", temperature=0)

@tool
def classify(text: str) -> str:
    """Classify text into one of: Coding, Writing, Research, or Summarization."""
    
    messages = [
        HumanMessage(content=f"""
        Classify the following text into exactly one of: Coding, Writing, Research, Summarization.
        Respond ONLY with the category name, no explanations.

        Text to classify: {text}
        """)
    ]

    try:
        response = model.invoke(messages)
        categories = ["Coding", "Writing", "Research", "Summarization"]
        result = response.strip()
        
        # Normalize the response
        for category in categories:
            if category.lower() in result.lower():
                return category
        return "Research"  # Default fallback

    except Exception as e:
        print(f"Error during classification: {e}")
        return "Research"
