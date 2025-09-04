from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize model
model = OllamaLLM(model="llama3.1:latest", temperature=0)

@tool
def classify(text: str) -> str:
    """
    Classifies the input text into one of the categories:
    Coding, Writing, Research, or Summarization.
    Always returns exactly one of these strings.
    """
    
    # Define prompt
    prompt_text = f"""
        You are an expert text classifier.
        Classify the following text into exactly one of: Coding, Writing, Research, Summarization.
        Respond ONLY with the category name, no explanations.

        Text to classify: {text}
        """
        # Use a single HumanMessage with all text
    messages = [HumanMessage(content=prompt_text)]
        

    
    try:
        # Call the Ollama model
        response = model.invoke(messages)
        print(f"Raw classification response: {response}")

        # Validate the output
        categories = ["Coding", "Writing", "Research", "Summarization"]
        result = response.strip()
        if result not in categories:
            print(f"Invalid category received: {result}. Defaulting to 'Research'.")
            return "Research"
        return result

    except Exception as e:
        print(f"Error during classification: {e}")
        return "Research"
