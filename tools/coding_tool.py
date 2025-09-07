from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize model
model = OllamaLLM(model="llama3.1:latest", temperature=0)

@tool
def coding(text: str) -> str:
    """
    This is a tool for coding-related tasks. If a task is classified as "Coding" by the classification tool,
    this tool will be used to handle the request. This tool will return "Claude" as the response and will also 
    give a psedo response for the request made.
    """
    
    # Define prompt
    prompt_text = f"""
        You are an expert programmer.
        Return the word "Claude" as the response.
        Also, Return a pseudo response which is not more than 50 words to the following coding task clearly and concisely:
        Text to classify: {text}

        If the user is not happy with this prompt, you can always ask them to rephrase their request.
        """
   

    
    try:
        # Call the Ollama model
        response = model.invoke([{"role": "user", "content": prompt_text}])
        result = response.strip()  # Clean up whitespace
        print(f"Raw coding tool response: {result}")
        return result

    except Exception as e:
        print(f"Error during coding tool execution: {e}")
        return "Error: Unable to process coding task."
