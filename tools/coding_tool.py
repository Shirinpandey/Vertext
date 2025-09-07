from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage

model = OllamaLLM(model="llama3.1:latest", temperature=0)

@tool
def coding(text: str) -> str:
    """Handle coding-related tasks and generate code solutions."""
    prompt_text = f"""
    You are an expert programmer. For this coding task:
    {text}
    
    Provide a code solution prefixed with 'CODE_SOLUTION:' followed by your implementation.
    Keep it concise and practical.
    """
    
    try:
        response = model.invoke([HumanMessage(content=prompt_text)])
        # Ensure response is prefixed properly
        if not response.startswith("CODE_SOLUTION:"):
            result = f"CODE_SOLUTION:\n{response}"
        else:
            result = response
        return result.strip()
    except Exception as e:
        return f"Error: {str(e)}"
